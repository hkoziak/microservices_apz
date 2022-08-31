from template import ServiceTemplate, FACADE_SERVICE_HOST, FACADE_SERVICE_PORT, MESSAGE_SERVICE_HOST, \
    MESSAGE_SERVICE_PORT, beautify_address
from flask import request, make_response
from threading import Thread
from msg_tool.msg_storage import MessageStorage, DistributedQueue, ServiceNotAvailable
import time
import sys


class MessageService(ServiceTemplate):
    def __init__(self, n):
        super().__init__("MessageService" + str(n))
        self.facade_service = None
        self.storage = MessageStorage()
        self.queue = DistributedQueue()
        self.id_for_msq = 500
        self.queue_msg = Thread(target=self.post_msg)
        self.queue_msg.daemon = True
        self.queue_msg.start()
        self.success = 200
        self.off = False

        @self.app.route("/", methods=['POST', 'GET'])
        def message():
            if request.method == 'POST':
                pass
            elif request.method == 'GET':
                answer = self.storage.get_all_msgs()
                return make_response(answer, self.success)

    def add_facade_service(self, path):
        self.facade_service = path

    def post_msg(self):
        while not self.off:
            time.sleep(10)
            if not self.queue.is_empty():
                try:
                    msg = self.queue.get_msg()
                    print(msg)
                    self.storage.save_msg(self.id_for_msq, msg)
                    self.id_for_msq += 1
                except ServiceNotAvailable as err:
                    print(err)


def main():
    if len(sys.argv) == 1:
        service = MessageService(1)
        port = MESSAGE_SERVICE_PORT
    elif len(sys.argv) == 3:
        service = MessageService(sys.argv[1])
        port = sys.argv[2]
    service.add_facade_service(beautify_address(FACADE_SERVICE_HOST, FACADE_SERVICE_PORT))
    service.run(MESSAGE_SERVICE_HOST, port)


if __name__ == "__main__":
    main()
