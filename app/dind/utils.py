import config
import os
from .lang import Language
import docker
import shutil
import logging


def initImages():
    client = docker.DockerClient(base_url=config.DOCKER_BASE_URL)
    for lang in Language:
        tmpPath = os.path.join(config.ROOT_DIR, config.TMP_DIR, lang.getTagname())
        os.mkdir(tmpPath)
        try:
            logging.info(f"Creating image {tmpPath}")
            dockerfile = open(
                os.path.join(
                    config.ROOT_DIR,
                    config.DOCKERFILES_DIR,
                    str(lang),
                    "base.Dockerfile",
                )
            ).read()

            with open(os.path.join(tmpPath, "Dockerfile"), "w") as file:
                file.write(dockerfile)

            client.images.build(path=tmpPath, tag=lang.getTagname(), rm=True)
        finally:
            logging.info(f"Done creating image {tmpPath}")
            for file in os.listdir(tmpPath):
                os.remove(os.path.join(tmpPath, file))
            os.rmdir(tmpPath)


def cleanTmpDir():
    tmpDir = os.path.join(config.ROOT_DIR, config.TMP_DIR)
    for file in os.listdir(tmpDir):
        if file == ".gitkeep":
            continue
        shutil.rmtree(os.path.join(tmpDir, file))
