from gevent.pywsgi import WSGIServer
from app.app import app
from app.dind.lang import Language
from app.dind.utils import initImages, cleanTmpDir
import logging


def clean():
    logging.info("Cleaning temporary directory.")
    cleanTmpDir()
    logging.info("Done cleaning temporary directory.")


def initialize():
    logging.info("Initializing base images.")
    initImages()
    logging.info("Done initializing base images.")


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    clean()
    initialize()
    http_server = WSGIServer(("0.0.0.0", 5000), app)
    logging.info("Started WSGI server.")
    http_server.serve_forever()
