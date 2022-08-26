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


    map = hz_client.get_map("my-distributed-map-locks")
    # start = time.time()
    key = '1'
    value = 0
    map.put_if_absent(key, value)
    for i in range(entries):
        value = map.get(key)
        # time.sleep(0.01)

        value = value.result() + 1
        map.put(key, value)

    print("Added to the distributed map")
    print(f"Result: {map.get(key).result()}")
    # print(f"Time: {time.time() - start}")

    # Shutdown the Hazelcast Client
    hz_client.shutdown()


if __name__ == "__main__":
    main()
