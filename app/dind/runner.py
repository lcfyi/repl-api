from time import sleep
import config
from .lang import Language
from .utils import clean_dir
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

        self.tmp_path = os.path.join(config.ROOT_DIR, config.TMP_DIR, self.filename)

        self.container = None
        self.image = None

    def init(self):
        os.mkdir(self.tmp_path)
        try:
            lang_dir = os.path.join(
                config.ROOT_DIR, config.DOCKERFILES_DIR, str(self.lang)
            )
            for file in os.listdir(lang_dir):
                tmp_contents = open(os.path.join(lang_dir, file)).read()
                if file == "Dockerfile":
                    tmp_contents = tmp_contents.replace("{}", config.DOCKER_BASE_IMAGE)
                with open(os.path.join(self.tmp_path, file), "w") as tmp_file:
                    tmp_file.write(tmp_contents)

            with open(os.path.join(self.tmp_path, "code"), "w") as tmp_file:
                tmp_file.write(self.code)

            self.image, _ = self.client.images.build(path=self.tmp_path, rm=True)
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
                    security_opt=["no-new-privileges=true"],
                )
                start = time.time()
                timeout = True
                while time.time() - start <= config.DOCKER_TIMEOUT_S:
                    time.sleep(0.2)
                    self.container.reload()
                    if self.container.status == "exited":
                        timeout = False
                        break
                if self.container.status == "running":
                    logging.warn(f"Container {self.filename} timed out, killing.")
                    try:
                        self.container.kill()
                    except docker.errors.APIError:
                        pass
                output = [
                    "...\n"
                    if i == config.MAX_LINES_RETURNED - 1
                    else line.decode("utf-8")
                    for i, line in enumerate(self.container.logs(stream=True))
                    if i < config.MAX_LINES_RETURNED
                ]
                if timeout:
                    if len(output):
                        output = ["Timed out. Output:\n"] + output
                    else:
                        output = ["Timed out."]
                return "".join(output)
            except docker.errors.ContainerError:
                return "Container failed to run!"
            finally:
                self.cleanup()
        else:
            # It shouldn't ever get to this point
            return "Build error."

    def cleanup(self):
        clean_dir(self.tmp_path)
        # We want both to try to run every time
        try:
            try:
                if self.container:
                    self.container.remove(force=True)
                if self.image:
                    self.client.images.remove(image=self.image.id, force=True)
            except AttributeError:
                if self.image:
                    self.client.images.remove(image=self.image.id, force=True)
        except discord.errors.APIError:
            pass