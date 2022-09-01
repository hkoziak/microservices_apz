from template import ServiceTemplate
from flask import request, make_response
from msg_tool.msg_storage import ServiceNotAvailable, DistributedMap
import sys
import consul


class LoggingService(ServiceTemplate):
    def __init__(self, n, host, port):
        super().__init__("LoggingService"+str(n), host, port)
        self.consul = consul.Consul()
        self.n = n
        self.map_name, self. map_node = None, None
        self.facades = []
        self.map_data()
        self.dmap = DistributedMap(self.map_node, self.map_name)
        self.register()
        self.register_facade()
        self.success = 200
        self.internal_error = 500

        @self.app.route("/", methods=['POST', 'GET'])
        def logging():
            if request.method == 'POST':
                uuid = request.json["uuid"]
                msg = request.json["msg"]
                try:
                    self.dmap.save_msg(uuid, msg)
                    print(msg)
                    return make_response("Posted successfully", self.success)
                except KeyError as err:
                    return make_response(str(err), 409)
                except ServiceNotAvailable as e:
                    return make_response(str(e), self.internal_error)
            elif request.method == 'GET':
                try:
                    return make_response(self.storage.get_all_msgs(), self.success)
                except ServiceNotAvailable as e:
                    return make_response(str(e), self.internal_error)

        @self.app.route("/health", methods=['GET'])
        def health():
            return make_response("healthy", 200)

    def register_facade(self):
        all = self.consul.agent.services()
        for k in all.keys():
            if all[k]['Service'] == 'facade':
                self.facade.append('http://' + all[k]['Address'] + '/')

    def register(self):
        url = "http://" + self.host + ":" + self.port + "/health"
        address = self.host + ":" + self.port
        self.consul.agent.service.register(name='logging', service_id=self.name, address=address,
                                           check=consul.Check.http(url=url, interval='30s'))

    def map_data(self):
        index, data = self.consul.kv.get('hz-map')
        self.map_name = data['Value'].decode('utf-8')

        index, data = self.consul.kv.get('hz.client_' + str(self.n))
        self.map_node = data['Value'].decode('utf-8')


def main():
    if len(sys.argv) != 4:
        print('Please enter only number, host and port separated with spaces')
    else:
        n, host, port = sys.argv[1], sys.argv[2], sys.argv[3]
    service = LoggingService(n, host, port)
    service.run()


if __name__ == "__main__":
    main()
