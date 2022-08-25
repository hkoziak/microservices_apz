from template import ServiceTemplate, FACADE_SERVICE_HOST, FACADE_SERVICE_PORT, LOGGING_SERVICE_HOST, \
    LOGGING_SERVICE_PORT, MESSAGE_SERVICE_HOST, MESSAGE_SERVICE_PORT, beautify_address
from flask import request, make_response
import requests


class FacadeService(ServiceTemplate):
    def __init__(self):
        super().__init__("FacadeService")
        self.logging_service, self.message_service = None, None
        self.uuid = 100

        @self.app.route("/", methods=['POST', 'GET'])
        def facade():
            internal_error = 500
            success = 200
            if request.method == 'GET':
                try:
                    part1 = requests.get(self.message_service)
                    part2 = requests.get(self.logging_service)
                except requests.exceptions.RequestException as message_get_err:
                    return make_response(f"Message Service Exception: {message_get_err}", internal_error)
                except requests.exceptions.RequestException as logging_get_err:
                    return make_response(f"Logging Service Exception: {logging_get_err}", internal_error)
                if part1.status_code != success or part2.status_code != success:
                    return make_response("Sorry, internal problems!", internal_error)
                answer = part1.text + "\n" + part2.text
                return make_response(f"GET request successful: {answer}", success)
            elif request.method == 'POST':
                message = request.json["message"]
                self.uuid += 1
                data = {"uuid": self.uuid, "msg": message}
                try:
                    requests.post(self.logging_service, json=data)
                except requests.exceptions.RequestException as logging_post_err:
                    return make_response(f"Logging Service Error{logging_post_err}", internal_error)
                return make_response("Post request successful:", success)

    def add_logging_service(self, path):
        self.logging_service = path

    def add_messages_service(self, path):
        self.message_service = path


def main():
    service = FacadeService()
    service.add_logging_service(beautify_address(LOGGING_SERVICE_HOST, LOGGING_SERVICE_PORT))
    service.add_messages_service(beautify_address(MESSAGE_SERVICE_HOST, MESSAGE_SERVICE_PORT))
    service.run(FACADE_SERVICE_HOST, FACADE_SERVICE_PORT)


if __name__ == "__main__":
    main()
