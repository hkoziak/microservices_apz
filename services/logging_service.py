from template import ServiceTemplate, FACADE_SERVICE_HOST, FACADE_SERVICE_PORT, LOGGING_SERVICE_HOST, \
    LOGGING_SERVICE_PORT, beautify_address
from flask import request, make_response
from msg_tool.msg_storage import MessageStorage


class LoggingServer(ServiceTemplate):
    def __init__(self, storage):
        super().__init__("LoggingService")
        self.storage = storage
        self.facade_service = None

        @self.app.route("/", methods=['POST', 'GET'])
        def logging():
            internal_error = 500
            success = 200
            if request.method == 'POST':
                uuid = request.json["uuid"]
                msg = request.json["msg"]
                try:
                    self.storage.save_msg(uuid, msg)
                    print(msg)
                    return make_response("OK", success)
                except KeyError as err:
                    return make_response(str(err), internal_error)
            elif request.method == 'GET':
                return make_response(self.storage.get_all_msgs(), success)

    def add_facade_service(self, path):
        self.facade_service = path


def main():
    storage = MessageStorage()
    service = LoggingServer(storage)
    service.add_facade_service(beautify_address(FACADE_SERVICE_HOST, FACADE_SERVICE_PORT))
    service.run(LOGGING_SERVICE_HOST, LOGGING_SERVICE_PORT)


if __name__ == "__main__":
    main()
