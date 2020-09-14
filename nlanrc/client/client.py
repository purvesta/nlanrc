import logging

import Pyro4
from client.lolcat.lolcat import LolCat


class Client:
    """nlanrc client class."""

    def __init__(self, server_ip, port):
        """Constructor."""
        self.log = logging.getLogger(__name__)
        self.registry_port = port
        self.server_ip = server_ip
        self.server = None

    def welcome(self):
        """Print welcome."""
        lol = LolCat()
        lol.cat("WELCOMEEEEEEE")

    def run(self):
        """Run the client interface."""
        uri = "PYRO:nlanrc.server@{}:{}".format(self.server_ip, self.registry_port)
        self.server = Pyro4.Proxy(uri)
        self.welcome()
        while True:
            command = input("nlanrc > ").strip()
            ret = self.run_command(command)
            if ret is None:
                print("Command doesn't exist.")
            if ret == -1:
                print("Invalid command syntax.")
            else:
                print(ret)

    def run_command(self, command):
        """Run the command given if it exists."""

        # Make sure we have the correct syntax
        if command[0] != "/":
            return -1

        if command[1:].lower() == "ping":
            return self.ping()
        elif command[1:].lower() == "exit":
            raise SystemExit

    def ping(self):
        self.log.debug("Sending PING")
        return self.server.ping()
