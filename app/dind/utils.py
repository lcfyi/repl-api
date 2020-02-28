import config
import os
from .lang import Language
import docker
import shutil
import logging


def init_images():
    client = docker.DockerClient(base_url=config.DOCKER_BASE_URL)
    for lang in Language:
        tmpPath = os.path.join(config.ROOT_DIR, config.TMP_DIR, lang.get_tag())
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

            client.images.build(path=tmpPath, tag=lang.get_tag(), rm=True)
        finally:
            logging.info(f"Done creating image {tmpPath}")
            for file in os.listdir(tmpPath):
                os.remove(os.path.join(tmpPath, file))
            os.rmdir(tmpPath)


def clean_tmp_dir():
    tmpDir = os.path.join(config.ROOT_DIR, config.TMP_DIR)
    for file in os.listdir(tmpDir):
        if file == ".gitkeep":
            continue
        shutil.rmtree(os.path.join(tmpDir, file))


def prune_images():
    client = docker.DockerClient(base_url=config.DOCKER_BASE_URL)
    client.images.prune()


def prune_containers():
    client = docker.DockerClient(base_url=config.DOCKER_BASE_URL)
    client.containers.prune()


def verify_valid_language(lang):
    try:
        Language[lang]
        return True
    except KeyError:
        return False
