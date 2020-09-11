import logging

import Pyro4


class Server:
    """nlanrc server class."""

    def __init__(self, port):
        """Constructor."""
        self.log = logging.getLogger(__name__)
        self.registry_port = int(port)
        self.server_ips = []
        self.is_coordinator = False
        # { uname: {uuid, ip, receivedTime, name, lastChangeDate } }
        self.user_data = dict()

    def serve(self):
        """Get the server up and running."""
        daemon = Pyro4.Daemon(host="localhost", port=self.registry_port)

        uri = daemon.register(self.ServerRequests, objectId="nlanrc.server")
        self.log.debug(uri)

        self.log.debug("Ready.")

        daemon.requestLoop()

    @Pyro4.expose
    class ServerRequests(object):
        def __init__(self):
            """Constructor."""
            self.log = logging.getLogger(__name__)

        def ping(self):
            """Pong method to call from client."""
            self.log.debug("Got PING, sending PONG")
            return "PONG!"
