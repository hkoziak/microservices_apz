from template import ServiceTemplate
from flask import request, make_response
from threading import Thread
from msg_tool.msg_storage import ServiceNotAvailable, DistributedQueue
import requests
import time
import random
import sys
import consul


class FacadeService(ServiceTemplate):
    def __init__(self, n, host, port):
        super().__init__("FacadeService" + str(n), host, port)
        self.consul = consul.Consul()
        self.log_services, self.msg_services = [], []
        self.log_quant, self.msg_quant = 0, 0
        self.uuid = 100
        self.queue_name = None
        self.turn_off = False
        self.uuid = 100
        self.internal_error = 500
        self.success = 200
        self.register()
        self.register_log_msg()
        self.get_queue_name()
        self.queue = DistributedQueue(self.queue_name)
        self.updater = Thread(target=self.update_log_services)
        self.updater.daemon = True
        self.updater.start()

        @self.app.route("/", methods=['POST', 'GET'])
        def facade():
            if request.method == 'GET':
                part1 = self.get_from_msg_server()
                part2 = self.get_from_log_server()
                if part1.status_code != self.success or part2.status_code != self.success:
                    return make_response("Something went wrong", self.internal_error)
                text = part2.text + part1.text
                return make_response(text, self.success)
            elif request.method == 'POST':
                message = request.json["message"]
                part1 = self.post_on_log_server(message)
                part2 = self.post_on_msg_server(message)
                if part1.status_code != self.success or part2.status_code != self.success:
                    return make_response("Internal Server Error", self.internal_error)
                return part1

        @self.app.route("/health", methods=['GET'])
        def health():
            return make_response("healthy", self.success)

    def update_log_services(self):
        while not self.turn_off:
            time.sleep(5)
            if (len(self.log_services) != self.log_quant) or (len(self.msg_services) != self.msg_quant):
                self.register_log_msg()

    def remove_log_service(self, path):
        self.log_services.remove(path)

    def remove_msg_service(self, msg_path):
        self.msg_services.remove(msg_path)

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

    def post_request(self, service, text):
        i = 0
        data = {"uuid": self.uuid + 1, "msg": text}
        try:
            response = requests.post(service, json=data)
        except requests.exceptions.RequestException as err:
            print("Logging service[", service, "]error:", err)
            raise ValueError
        while i < 10:
            if response.status_code == self.success:
                break
            elif response.status_code == 409:
                self.uuid += 10
                i += 1
            else:
                return make_response(f"Internal Service Error {response.text}", self.internal_error)
            data = {"uuid": self.uuid + 1, "msg": text}
            try:
                response = requests.post(service, json=data)
            except requests.exceptions.RequestException as err:
                print("Logging service[ ", service, " ] error:", err)
                return make_response("Internal Service Error", self.internal_error)
        self.uuid += 1
        return make_response("Success", self.success)

    def post_on_log_server(self, msg):
        while True:
            log_service = random.choice(self.logging_services)
            response = self.post_request(log_service, msg)
            if response.status_code == 200:
                break
            else:
                self.remove_log_service(log_service)
        return response

    def post_on_msg_server(self, msg):
        try:
            self.queue.put_msg(msg)
        except ServiceNotAvailable as err:
            return make_response(str(err), self.internal_error)
        return make_response("Success", self.success)

    def get_from_log_server(self):
        while True:
            log_service = random.choice(self.logging_services)
            ans = self.get_request(log_service, "Logging")
            if ans.status_code == self.success:
                break
            else:
                self.remove_log_service(log_service)
        return ans

    def get_from_msg_server(self):
        while True:
            msg_server = random.choice(self.message_services)
            ans = self.get_request(msg_server, "Message")
            if ans.status_code == self.success:
                break
            else:
                self.remove_msg_service(msg_server)
        return ans

    def register_log_msg(self):
        all_services = self.consul.agent.services()
        log_temp, msg_temp = [], []
        for k in all_services.keys():
            if all_services[k]['Service'] == 'logging':
                log_temp.append('http://' + all_services[k]['Address'] + "/")
            elif all_services[k]['Service'] == 'message':
                msg_temp.append('http://' + all_services[k]['Address'] + "/")
        self.log_services, self.msg_services = log_temp, msg_temp
        self.log_quant, self.msg_quant = len(self.log_services), len(self.msg_services)

    def get_queue_name(self):
        index, data = self.consul.kv.get('hz-mq')
        self.queue_name = data['Value'].decode('utf-8')

    def register(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        address = self.host + ":" + self.port
        self.consul.agent.service.register(name='facade', service_id=self.name, address=address,
                                           check=consul.Check.http(url=url, interval='30s'))


def main():
    if len(sys.argv) != 4:
        print('Please enter only number, host and port separated with spaces')
    else:
        n, host, port = sys.argv[1], sys.argv[2], sys.argv[3]
    service = FacadeService(n, host, port)
    service.run()


if __name__ == "__main__":
    main()
