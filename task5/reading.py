import hazelcast
import time


def main():
    entries = 1000
    hz_client = hazelcast.HazelcastClient(cluster_name="dev",
                                          cluster_members=[
                                               "127.0.0.1:5702",
                                               "127.0.0.1:5703"
                                           ])
    print("Established connection to dev cluster")


    bq = hz_client.get_queue("new_bounded_queue").blocking()
    for i in range(entries):
        value = bq.take()
        if i % 100 == 0:
            print(f"Reading in process. Currently on value: {value}")
        time.sleep(0.01)


    hz_client.shutdown()


if __name__ == "__main__":
    main()
