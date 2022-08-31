from services.template import FACADE_SERVICE_HOST, FACADE_SERVICE_PORT, beautify_address
import requests


class Client:
    def __init__(self):
        self.url = beautify_address(FACADE_SERVICE_HOST, FACADE_SERVICE_PORT)

    def post_message(self, msg):
        info = {"message": msg}
        try:
            response = requests.post(self.url, json=info)
        except requests.exceptions.RequestException as err:
            return 0, err
        return response.status_code, response.text

    def get_info(self):
        try:
            response = requests.get(self.url)
        except requests.exceptions.RequestException as err:
            return 0, err
        return response.status_code, response.text


def main():
    client = Client()
    success = 200
    text = ""
    print("Lab1 (microservices). Enter 'stop' to exit\n")
    while text.lower() != "stop":
        text = input("'POST' or 'GET': ")
        if text.lower() == "post":
            msg = input("Enter your message: ")
            result = client.post_message(msg)
            if result[0] != success:
                print("Something went wrong,", result[1])
            else:
                print("Success\n")
        elif text.lower() == "get":
            result = client.get_info()
            if result[0] != success:
                print("Something went wrong,", result[1])
            else:
                print(str(result[1]) + "\n")
        elif text.lower() == "stop":
            pass
        else:
            print("Choose a correct method or enter 'stop' to exit\n")
    return


if __name__ == "__main__":
    main()
