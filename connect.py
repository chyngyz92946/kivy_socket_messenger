import threading
import socket
import sys


class Server:

    connections = []

    def __init__(self, port, host="localhost"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)

    def handler(self, c, a):
        print("Пользователь подключен: {0} : {1}".format(c, a))
        while True:
            data = c.recv(1024)
            for con in self.connections:
                con.send(data)
            if not data:
                break
            print(data)

    def run(self):
        while True:
            c, a = self.socket.accept()
            cThread = threading.Thread(target=self.handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(a)


class Client:
    message = ""
    message_read = ""
    def __init__(self, port, host="localhost"):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host
        self.socket.connect((self.host, self.port))

    def sen_message(self):
        while True:
            if self.message != "":
                self.socket.send(bytes(self.message, "utf-8"))
                self.message = ""


    def run(self):
        cThread = threading.Thread(target=self.sen_message)
        cThread.daemon = True
        cThread.start()
        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            print(data)
            self.message_read = data.decode("utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        client = Client(8080, host=sys.argv[1])
        client.run()
    else:
        ser = Server(8080, host="127.0.0.1")
        ser.run()


