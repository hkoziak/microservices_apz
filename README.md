# Lab work 1: microservices basics
Authors (team): [Halyna Koziak](https://github.com/hkoziak)

### Before

You need to have <b>Flask</b> package installed and <b>Python 3</b> for running this app.   
You may use client in terminal (described below), Postman or other service.

### Launching
Launch 3 hazelcast nodes. You have to pass the number of node and the address to each separate logging service.
If running on localhost, the first logging service will pick-up number and node automatically.
Example of run of the logging service:   
```python3 services/logging_service.py 2 127.0.0.1:5702```   
Launch Message service:   
```python3 services/message_service.py```   
Launch Facade service passing adresses of logging services. **Separate them with semi-colon, not whitespace, and include ```http://```**:
```
python3 services/facade_service.py http://127.0.0.1:3001;http://127.0.0.1:3003;http://127.0.0.1:3004
```
  
You may change pre-defined hosts and ports in file <b>services/template.py</b>.

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
![alt text](https://github.com/hkoziak/microservices_apz/blob/micro_basics/run.png?raw=true)


