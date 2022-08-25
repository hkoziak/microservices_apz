# Lab work 1: microservices basics
Authors (team): [Halyna Koziak](https://github.com/hkoziak)

### Before

You need to have <b>Flask</b> package installed and <b>Python 3</b> for running this app.   
You may use client in terminal (described below), Postman or other service.

### Launching
Launch Facade, Logging and Message services in separate windows with this commands:
```
python3 services/facade_service.py
python3 services/logging_service.py
python3 services/message_service.py
```
They will be running on <b>127.0.0.1</b>, ports 3000, 3001, 3002.    
You may change hosts and ports in file <b>services/template.py</b>.

To run a client in terminal window use the next command:
```
python3 main.py
```

### Usage

Send POST or GET HTTP calls to facade service. GET call doesn't have any params,   
POST call must contain json body with "message" field: ```{"message": "hi"}```.
Example of use and output:   
![alt text](https://github.com/hkoziak/microservices_apz/blob/micro_basics/Example_of_use.png?raw=true)


