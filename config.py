import os

DOCKER_BASE_URL = "tcp://docker:2375"
DOCKER_MAX_MEM = "256m"
DOCKER_MAX_CPU = "0"
DOCKER_MAX_PID = 64
DOCKER_TIMEOUT_S = 10

DOCKER_ULIMIT_NPROC = 64
DOCKER_ULIMIT_CORE = 0
DOCKER_ULIMIT_FSIZE = 20000
DOCKER_ULIMIT_CPU = 20

WSGI_MAX_CONNECTIONS = 10

MAX_LINES_RETURNED = 50

TMP_DIR = "tmp"

DOCKERFILES_DIR = "dockerfiles"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
