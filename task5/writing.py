import hazelcast
import time


def main():
    entries = 1000
    hz_client = hazelcast.HazelcastClient(cluster_name="dev",
                                          cluster_members=[
                                               "127.0.0.1:5701",
                                          ])
    print("Established connection to dev cluster")


    bq = hz_client.get_queue("new_bounded_queue").blocking()
    for i in range(entries):
        bq.put(str(i))
        if i % 100 == 0:
            print(f"Writing in process. Currently on value: {i}")
        time.sleep(0.01)


    hz_client.shutdown()


if __name__ == "__main__":
    main()
