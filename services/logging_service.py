from template import ServiceTemplate, FACADE_SERVICE_HOST, FACADE_SERVICE_PORT, LOGGING_SERVICE_HOST, \
    LOGGING_SERVICE_PORT, STORAGE_NODE_FOR_1, beautify_address
from flask import request, make_response
from msg_tool.msg_storage import ServiceNotAvailable, DistributedMap
import sys


class LoggingServer(ServiceTemplate):
    def __init__(self, n, node):
        super().__init__("LoggingService"+str(n))
        self.storage = DistributedMap(node, "HZ_map")
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
                    return make_response("Posted successfully", success)
                except KeyError as err:
                    return make_response(str(err), 409)
                except ServiceNotAvailable as e:
                    return make_response(str(e), internal_error)
            elif request.method == 'GET':
                try:
                    return make_response(self.storage.get_all_msgs(), success)
                except ServiceNotAvailable as e:
                    return make_response(str(e), internal_error)

    def add_facade_service(self, path):
        self.facade_service = path


def main():
    if len(sys.argv) == 1:
        service = LoggingServer(1, STORAGE_NODE_FOR_1)
        port = LOGGING_SERVICE_PORT
    elif len(sys.argv) == 4:
        service = LoggingServer(sys.argv[1], sys.argv[2])
        port = sys.argv[3]
    service.add_facade_service(beautify_address(FACADE_SERVICE_HOST, FACADE_SERVICE_PORT))
    service.run(LOGGING_SERVICE_HOST, port)


if __name__ == "__main__":
    main()
