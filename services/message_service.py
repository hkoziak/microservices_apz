from template import ServiceTemplate
from flask import request, make_response
from threading import Thread
from msg_tool.msg_storage import MessageStorage, DistributedQueue, ServiceNotAvailable
import time
import sys
import consul


class MessageService(ServiceTemplate):
    def __init__(self, n):
        super().__init__("MessageService" + str(n), host, port)
        self.consul = consul.Consul()
        self.facade = []
        self.success = 200
        self.storage = MessageStorage()
        self.queue_name = None
        self.id_for_msg = 500
        self.off = False
        self.register()
        self.add_facade_service()
        self.queue_data()
        self.queue = DistributedQueue(self.queue_name)
        self.queue_msg = Thread(target=self.post_msg)
        self.queue_msg.daemon = True
        self.queue_msg.start()

        self.facade = None

        @self.app.route("/", methods=['POST', 'GET'])
        def message():
            if request.method == 'POST':
                pass
            elif request.method == 'GET':
                answer = self.storage.get_all_msgs()
                return make_response(answer, self.success)

        @self.app.route("/health", methods=['GET'])
        def health():
            return make_response("healthy", 200)

    def register(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        address = self.host + ":" + self.port
        self.consul.agent.service.register(name='message', service_id=self.name, address=address,
                                           check=consul.Check.http(url=url, interval='30s'))

    def add_facade_service(self, path):
        all = self.consul.agent.services()
        for k in all.keys():
            if all[k]['Service'] == 'facade':
                self.facade.append('http://' + all[k]['Address'] + '/')

    def post_msg(self):
        while not self.off:
            time.sleep(10)
            if not self.queue.is_empty():
                try:
                    msg = self.queue.get_msg()
                    print(msg)
                    self.storage.save_msg(self.id_for_msg, msg)
                    self.id_for_msg += 1
                except ServiceNotAvailable as err:
                    print(err)

    def queue_data(self):
        index, data = self.consul.kv.get('hz-mq')
        self.queue_name = data['Value'].decode('utf-8')


def main():
    if len(sys.argv) != 4:
        print('Please enter only number, host and port separated with spaces')
    else:
        n, host, port = sys.argv[1], sys.argv[2], sys.argv[3]
    service = MessageService(n, host, port)
    service.run()


if __name__ == "__main__":
    main()
