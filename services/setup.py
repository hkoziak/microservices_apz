import consul


def main():
    consul_kv = consul.Consul()
    consul_kv.kv.put('hz.client_0', '127.0.0.1:5701')
    consul_kv.kv.put('hz.client_1', '127.0.0.1:5702')
    consul_kv.kv.put('hz.client_2', '127.0.0.1:5703')
    consul_kv.kv.put('hz-map', 'log_distributed_map')
    consul_kv.kv.put('hz-mq', 'msg_distributed_queue')


if __name__ == "__main__":
    main()
