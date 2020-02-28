from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from gevent.pool import Pool
from app.app import app
from app.dind.lang import Language
from app.dind.utils import (
    init_images,
    clean_tmp_dir,
    prune_containers,
    prune_images,
    wait_for_connection,
)
import logging
import config
import sys


def clean():
    logging.info("Cleaning temporary directory.")
    clean_tmp_dir()
    prune_containers()
    prune_images()
    logging.info("Done cleaning temporary directory.")


def initialize():
    logging.info("Initializing base images.")
    init_images()
    logging.info("Done initializing base images.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    if not wait_for_connection(config.DOCKER_CONNECTION_RETRIES):
        sys.exit(1)
    clean()
    initialize()
    pool = Pool(config.WSGI_MAX_CONNECTIONS)
    http_server = WSGIServer(("0.0.0.0", 5000), app, spawn=pool)
    logging.info("Started WSGI server.")
    http_server.serve_forever()
