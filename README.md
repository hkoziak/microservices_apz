# Lab work 1: microservices basics
Authors (team): [Halyna Koziak](https://github.com/hkoziak)

### Report
Code is in Python so before running, install hazelcast package:   
```pip install hazelcast-python-client```

**1-2 tasks done:**    
I installed Hazelcast and launched a cluster containing 3 nodes:   
![alt text](https://github.com/hkoziak/microservices_apz/blob/hazelcast_lab/report_images/tasks1_2.png?raw=true)

**3 task:**   

Distributed Map (code can be found in file task3.py)
In all cases data was distributed almost perfectly, no data loss was observed.   
3 nodes:
![alt text](https://github.com/hkoziak/microservices_apz/blob/hazelcast_lab/report_images/task3_3nodes.png?raw=true)

After shutting down 1 node:
![alt text](https://github.com/hkoziak/microservices_apz/blob/hazelcast_lab/report_images/task3_2nodes.png?raw=true)

After shutting down 2 nodes:
![alt text](https://github.com/hkoziak/microservices_apz/blob/hazelcast_lab/report_images/task3_1node.png?raw=true)

**4 task:** 
Code for map without, with optimistic and pessimistic one may be found in folder 4.   
Pessimistic blocking is the longest; optimistic is around 2 times faster, and with no blocking is the fastest way.
However, without use of blocking we observe a race.
Results are like this:
![alt text](https://github.com/hkoziak/microservices_apz/blob/hazelcast_lab/report_images/task4_no_blocking.png?raw=true)

**5 task:** 