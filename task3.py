import hazelcast


def main():
    entries = 1000
    hz_client = hazelcast.HazelcastClient(cluster_name="dev",
                                          cluster_members=[
                                           "127.0.0.1:5701",
                                           "127.0.0.1:5702",
                                           "127.0.0.1:5703"
                                          ])
    print("Established connection to dev cluster")

    # Getting the distributed map
    map = hz_client.get_map("my-distributed-map").blocking()
    for i in range(entries):
        map.put(i, f"entry_{i}")
    print("Data is imported")

    # Shutdown the Hazelcast Client
    hz_client.shutdown()


if __name__ == "__main__":
    main()
