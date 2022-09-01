# Lab work 1: microservices basics
Authors (team): [Halyna Koziak](https://github.com/hkoziak)

### Before

You need to have <b>Flask</b> package installed and <b>Python 3</b> for running this app.   
You may use client in terminal (described below), Postman or other service.

### Launching
Launch 3 hazelcast nodes.
Python package for Consul can be installed with ```pip3 install python-consul```
Then launch **setup.py**. 
```
python3 services/setup.py
```
Then launch message, logging and facade services, providing as args number of this service, host and port separated with whitespaces:   
```
python3 services/logging_service.py 2 127.0.0.1 3002
```

To run a client in terminal window use the next command:
```
python3 main.py
```

### Usage

Send POST or GET HTTP calls to facade service. GET call doesn't have any params,   
POST call must contain json body with "message" field: ```{"message": "hi"}```.
Example of use and output:   
![alt text](https://github.com/hkoziak/microservices_apz/blob/micro_basics/Example_of_use.png?raw=true)

**Updated:**
![alt text](https://github.com/hkoziak/microservices_apz/blob/micro_mq/run1.png?raw=true)


