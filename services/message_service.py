from template import ServiceTemplate, FACADE_SERVICE_HOST, FACADE_SERVICE_PORT, MESSAGE_SERVICE_HOST, \
    MESSAGE_SERVICE_PORT, beautify_address
from flask import request, make_response


class MessageServer(ServiceTemplate):
    def __init__(self):
        super().__init__("MessageService")
        self.facade_service = None

        @self.app.route("/", methods=['POST', 'GET'])
        def message():
            if request.method == 'POST':
                pass
            elif request.method == 'GET':
                return make_response("not implemented yet", 200)

    def add_facade_service(self, path):
        self.facade_service = path


def main():
    server = MessageServer()
    server.add_facade_service(beautify_address(FACADE_SERVICE_HOST, FACADE_SERVICE_PORT))
    server.run(MESSAGE_SERVICE_HOST, MESSAGE_SERVICE_PORT)


if __name__ == "__main__":
    main()
