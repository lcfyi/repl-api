from time import sleep
import config
from .lang import Language
import docker
import logging
import os
import time


class CodeRunner:
    def __init__(self, language, code):
        self.lang = Language[language]
        self.code = code
        self.filename = f"tmp{hash(self)}"
        self.client = docker.DockerClient(base_url=config.DOCKER_BASE_URL)

        self.tmpPath = os.path.join(config.ROOT_DIR, config.TMP_DIR, self.filename)

        self.container = None
        self.image = None

    def init(self):
        os.mkdir(self.tmpPath)
        try:
            dockerfile = (
                open(
                    os.path.join(
                        config.ROOT_DIR,
                        config.DOCKERFILES_DIR,
                        str(self.lang),
                        "base.Dockerfile",
                    )
                ).read()
                + open(
                    os.path.join(
                        config.ROOT_DIR,
                        config.DOCKERFILES_DIR,
                        str(self.lang),
                        "code.Dockerfile",
                    )
                ).read()
            )
            with open(os.path.join(self.tmpPath, "Dockerfile"), "w") as file:
                file.write(dockerfile)

            with open(os.path.join(self.tmpPath, "code"), "w") as file:
                file.write(self.code)

            self.image, _ = self.client.images.build(path=self.tmpPath, rm=True)
        except Exception as e:
            logging.error(e)
            self.cleanup()

    def run(self):
        self.init()
        if self.image:
            try:
                nproc_limit = docker.types.Ulimit(
                    name="nproc",
                    soft=config.DOCKER_ULIMIT_NPROC,
                    hard=config.DOCKER_ULIMIT_NPROC,
                )
                core_limit = docker.types.Ulimit(
                    name="core",
                    soft=config.DOCKER_ULIMIT_CORE,
                    hard=config.DOCKER_ULIMIT_CORE,
                )
                fsize_limit = docker.types.Ulimit(
                    name="fsize",
                    soft=config.DOCKER_ULIMIT_FSIZE,
                    hard=config.DOCKER_ULIMIT_FSIZE,
                )
                cpu_limit = docker.types.Ulimit(
                    name="cpu",
                    soft=config.DOCKER_ULIMIT_CPU,
                    hard=config.DOCKER_ULIMIT_CPU,
                )

                self.container = self.client.containers.run(
                    image=self.image.id,
                    mem_limit=config.DOCKER_MAX_MEM,
                    cpuset_cpus=config.DOCKER_MAX_CPU,
                    pids_limit=config.DOCKER_MAX_PID,
                    detach=True,
                    ulimits=[nproc_limit, core_limit, fsize_limit, cpu_limit],
                )
                start = time.time()
                while time.time() - start <= config.DOCKER_TIMEOUT_S:
                    time.sleep(0.2)
                    self.container.reload()
                    if self.container.status == "exited":
                        break
                if self.container.status == "running":
                    logging.warn(f"Container {self.filename} timed out, killing.")
                    try:
                        self.container.kill()
                    except docker.errors.APIError:
                        # TODO do some manual cleanup
                        pass
                return "".join(
                    [
                        "...\n"
                        if i == config.MAX_LINES_RETURNED - 1
                        else line.decode("utf-8")
                        for i, line in enumerate(self.container.logs(stream=True))
                        if i < config.MAX_LINES_RETURNED
                    ]
                )
            except docker.errors.ContainerError:
                return "Container failed to run!"
            finally:
                self.cleanup()

    def cleanup(self):
        for file in os.listdir(self.tmpPath):
            os.remove(os.path.join(self.tmpPath, file))
        os.rmdir(self.tmpPath)
        try:
            self.container.remove(force=True)
            self.client.images.remove(image=self.image.id)
        except AttributeError:
            self.client.images.remove(image=self.image.id)
        except docker.errors.APIError:
            # TODO do some manual cleanup
            pass
