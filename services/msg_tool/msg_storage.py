import hazelcast


class MessageStorage:
    def __init__(self):
        self.storage = {}

    def save_msg(self, uuid, msg):
        if uuid not in self.map.keys():
            self.storage[uuid] = msg
        raise KeyError("Such id already exists")

    def get_all_msgs(self):
        msgs = ""
        for k in self.storage.keys():
            msgs += self.storage[k] + "\n"
        return msgs


class ServiceNotAvailable(Exception):
    def __init__(self, msg="Hazelcast node not connected"):
        self.msg = msg
        super().__init__(self.msg)


class DistributedMap:
    def __init__(self, storage_node, map_name):
        try:
            self.hz = hazelcast.HazelcastClient(cluster_members=[
                storage_node
            ], cluster_connect_timeout=100)
            self.map = self.hz.get_map(map_name).blocking()
        except hazelcast.errors.IllegalStateError:
            print("Unable to connect to Hazelcast")
            self.map = None

    def save_msg(self, uuid, msg):
        if self.map is None:
            raise ServiceNotAvailable
        try:
            if not self.map.contains_key(uuid):
                self.map.put(uuid, msg)
            raise KeyError("Key is already in map")
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise ServiceNotAvailable

    def get_all_msgs(self):
        if self.map is None:
            raise ServiceNotAvailable
        try:
            values = self.map.values()
            return "\n".join(values) + "\n"
        except hazelcast.errors.TargetDisconnectedError as err:
            print(err)
            raise ServiceNotAvailable


class DistributedQueue:
    def __init__(self):
        try:
            self.hz = hazelcast.HazelcastClient()
            self.queue = self.hz.get_queue("my-mq").blocking()
        except hazelcast.errors.IllegalStateError:
            raise ServiceNotAvailable

    def get_msg(self):
        if self.queue is None:
            raise ServiceNotAvailable
        return self.queue.poll()

    def put_msg(self, msg):
        if self.queue is None:
            raise ServiceNotAvailable
        self.queue.put(msg)

    def is_empty(self):
        if self.queue is None:
            raise ServiceNotAvailable
        return self.queue.is_empty()
