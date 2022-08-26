import hazelcast
import time


def main():
    entries = 1000
    hz_client = hazelcast.HazelcastClient(cluster_name="dev",
                                          cluster_members=[
                                              "127.0.0.1:5701",
                                              "127.0.0.1:5702",
                                              "127.0.0.1:5703"
                                          ])
    print("Established connection to dev cluster")


    map = hz_client.get_map("my-distributed-map-locks").blocking()
    key = '1'
    value = 0
    # start = time.time()
    map.put_if_absent(key, value)
    for i in range(entries):
        map.lock(key)
        try:
            value = map.get(key)
            time.sleep(0.01)

            value += 1
            map.put(key, value)
        finally:
            map.unlock(key)

    print("Added to the distributed map")
    print(f"Result: {map.get(key)}")
    # print(f"Time: {time.time() - start}")

    # Shutdown the Hazelcast Client
    hz_client.shutdown()


if __name__ == "__main__":
    main()
