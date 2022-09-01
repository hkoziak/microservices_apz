from flask import Flask


class ServiceTemplate:
    def __init__(self, name, host, port):
        self.app = Flask(name)
        self.name = name
        self.host = host
        self.port = port

    def run(self):
        self.app.run(host=self.host, port=self.port)


# a few constants
# FACADE_SERVICE_HOST = "127.0.0.1"
# FACADE_SERVICE_PORT = 3000
# LOGGING_SERVICE_HOST = "127.0.0.1"
# LOGGING_SERVICE_PORT = 3001
# MESSAGE_SERVICE_HOST = "127.0.0.1"
# MESSAGE_SERVICE_PORT = 3002
#
# STORAGE_NODE_FOR_1 = "127.0.0.1:5701"


def beautify_address(host, port):
    return f"http://{host}:{port}/"
