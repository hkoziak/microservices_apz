from template import ServiceTemplate, FACADE_SERVICE_HOST, FACADE_SERVICE_PORT, LOGGING_SERVICE_HOST, \
    LOGGING_SERVICE_PORT, MESSAGE_SERVICE_HOST, MESSAGE_SERVICE_PORT, beautify_address
from flask import request, make_response
from threading import Thread
import requests
import time
import random
import sys


class FacadeService(ServiceTemplate):
    def __init__(self):
        super().__init__("FacadeService")
        self.logging_services, self.log_services_off = [], []
        self.message_service = None
        self.turn_off = False
        self.uuid = 100
        self.updater = Thread(target=self.update_log_services)
        self.updater.daemon = True
        self.updater.start()
        self.internal_error = 500
        self.success = 200

        @self.app.route("/", methods=['POST', 'GET'])
        def facade():
            if request.method == 'GET':
                part1 = self.get_request(self.message_service, "Message")
                try:
                    while True:
                        log_service = random.choice(self.logging_services)
                        part2 = self.get_request(log_service, "Log")
                        if part2.status_code == self.success:
                            break
                        else:
                            self.remove_log_service(log_service)
                except IndexError:
                    part2 = make_response("Service error", self.internal_error)
                if part1.status_code != self.success or part2.status_code != self.success:
                    return make_response("Sorry, internal problems!", self.internal_error)
                answer = part1.text + "\n" + part2.text
                return make_response(f"GET request successful: {answer}", self.success)
            elif request.method == 'POST':
                message = request.json["message"]
                try:
                    while True:
                        log_server = random.choice(self.logging_services)
                        i = 0
                        data = {"uuid": self.uuid + 1, "msg": message}
                        try:
                            response = requests.post(log_server, json=data)
                        except requests.exceptions.RequestException as e:
                            print("Logging service[ ", log_server, " ]error:", e)
                            return make_response("Internal Service Error", self.internal_error)
                        while i < 10:
                            if response.status_code == self.success:
                                break
                            elif response.status_code == 409:
                                self.uuid += 10
                                i += 1
                            else:
                                print("Logging service[", log_server, "] POST request error:", response.status_code, response.text)
                                return make_response("Internal Service Error", self.internal_error)
                            data = {"uuid": self.uuid + 1, "msg": message}
                            try:
                                response = requests.post(log_server, json=data)
                            except requests.exceptions.RequestException as err:
                                print("Logging service[", log_server, "] error:", err)
                                return make_response("Internal Service Error", self.internal_error)
                        self.uuid += 1
                        response = make_response("Message successfully posted", self.success)
                        if response.status_code == self.success:
                            break
                        else:
                            self.remove_log_service(log_server)
                except IndexError:
                    response = make_response("Service error", self.internal_error)
                return response

    def update_log_services(self):
        while not self.turn_off:
            time.sleep(5)
            restored = []
            for service in self.log_services_off:
                try:
                    response = requests.get(service)
                except requests.exceptions.RequestException:
                    continue
                if response.status_code == self.success:
                    self.add_logging_service(service)
                    restored.append(service)
            for service in restored:
                self.log_services_off.remove(service)

    def add_logging_service(self, path):
        self.logging_services.append(path)

    def remove_log_service(self, path):
        self.logging_services.remove(path)
        self.log_services_off.append(path)

    def add_messages_service(self, path):
        self.message_service = path

    def get_request(self, service, server_type):
        try:
            response = requests.get(service)
        except requests.exceptions.RequestException as err:
            print(server_type, "service[", service, "] error:", err)
            return make_response("Service Exception", self.internal_error)
        if response.status_code != self.success:
            print(server_type, "service[", service, "] GET request error:", response.status_code, response.text)
            return make_response("Service Exception", self.internal_error)
        return response


def main():
    service = FacadeService()
    if len(sys.argv) == 1:
        service.add_logging_service(beautify_address(LOGGING_SERVICE_HOST, LOGGING_SERVICE_PORT))
    elif len(sys.argv) == 2:
        log_services = sys.argv[1].split(";")
        for i in log_services:
            service.add_logging_service(i)
    service.add_messages_service(beautify_address(MESSAGE_SERVICE_HOST, MESSAGE_SERVICE_PORT))
    service.run(FACADE_SERVICE_HOST, FACADE_SERVICE_PORT)


if __name__ == "__main__":
    main()
