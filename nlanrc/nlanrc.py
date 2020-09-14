"""
nlanrc


    Usage:
        nlanrc.py server [-p <port>] [--level=<level>]
        nlanrc.py client (-s | --server) <server_ip> [-p <port>] [--level=<level>]
        nlanrc.py (-h | --help)
        nlanrc.py --version
    Options:
        -h --help           Show this screen.
        -l --level=<level>  Logging level. [default: WARNING]
        -p --port=<port>    Port to host on or connect to. [default: 4444]
        -s --server         Server ip address to connect to.
        --version           Show version.

"""

import logging
from logging import StreamHandler

from client.client import Client
from docopt import docopt
from server.server import Server

__version__ = "0.0.1"


def main():
    arguments = docopt(__doc__, version=__version__)

    level = getattr(logging, arguments.get("--level").upper())

    handlers = [StreamHandler()]
    log = logging.getLogger(__name__)
    logging.basicConfig(level=level, format="%(asctime)s %(name)-15s: %(levelname)-8s %(message)s", handlers=handlers)

    port = arguments.get("--port")

    # Are we a server or a client?
    if arguments.get("server"):
        log.debug("We are a server!")
        log.debug("Running on: {} port: {}".format("localhost", port))
        server = Server(port)
        server.serve()
    else:
        server_ip = arguments.get("<server_ip>")
        log.debug("We are a client!")
        log.debug("Running on: {} port: {}".format(server_ip, port))
        client = Client(server_ip, port)
        client.run()


if __name__ == "__main__":
    main()
