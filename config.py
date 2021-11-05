import os

DOCKER_BASE_URL = "unix://var/run/docker.sock"
DOCKER_MAX_MEM = "256m"
DOCKER_MAX_CPU = "0"
DOCKER_MAX_PID = 64
DOCKER_TIMEOUT_S = 10
DOCKER_CONNECTION_RETRIES = 5

DOCKER_ULIMIT_NPROC = 64
DOCKER_ULIMIT_CORE = 0
DOCKER_ULIMIT_FSIZE = 20000
DOCKER_ULIMIT_CPU = 20
DOCKER_DISABLE_NETWORKING = True

DOCKER_BASE_IMAGE = "base-image"

WSGI_MAX_CONNECTIONS = 10

MAX_LINES_RETURNED = 50

TMP_DIR = "tmp"

DOCKERFILES_DIR = "dockerfiles"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
