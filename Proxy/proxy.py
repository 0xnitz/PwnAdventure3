import threading
import socket

class asyncSocketClient:
    BUFFER_SIZE = 1024

    def __init__(self, clientIp, clientPort, mainpulationFunc):
        self.clientIp   = clientIp
        self.clientPort = clientPort
        self.sock       = None

    def initialize(self):
        self.sock = socket.socket()
        self.sock.connect((self.clientIp, self.clientPort))

    def send(self, data):
        data = self.mainpulationFunc(data)
        self.send(data)

class asyncSocketServer:
    BUFFER_SIZE = 1024

    def __init__(self, serverPort, mainpulationFunc):
        self.clientIp = clientIp
        self.serverIp = serverIp
        self.isServer = isServer
        self.sock     = None

    def start(self):
        self.sock = socket.socket()

        if not isServer:
            self.sock.connect((self.serverIp, self.serverPort))
        else:
            self.sock.listen(1)
            self.sock.bind(('', serverPort))

def handler_doNothing(txt):
        return txt

class proxy:
    def __init__(self, serverIp, serverPort, clientIp, clientPort, clientManipulation=handler_doNothing, serverManipulation=handler_doNothing):
        self.serverIp           = serverIp
        self.serverPort         = serverPort
        self.clientIp           = clientIp
        self.clientPort         = clientPort
        self.threads            = []
        self.clientManipulation = clientManipulation
        self.serverManipulation = serverManipulation

        self.clientSock = socket.socket()
        self.listenSock = socket.socket()

    def initialize(self):
        print 'Waiting for client'
        self.listenSock.bind(('', self.clientPort))
        self.listenSock.listen(1)
        c, addr = self.listenSock.accept()
        self.serverSock = c

        print 'Connecting server'
        self.clientSock.connect((self.serverIp, self.serverPort))

    def serverRunner(self):
        data = self.serverSock.recv(1024)
        data = self.serverManipulation(data)
        self.clientSock.send(data)

    def clientRunner(self):
        data = self.clientSock.recv(1024)
        data = self.clientManipulation(data)
        self.serverSock.send(data)

    def start(self):
        tClient = threading.Thread(target=self.clientRunner)
        tServer = threading.Thread(target=self.serverRunner)

        self.threads.append(tClient)
        self.threads.append(tServer)

        tServer.start()
        tClient.start()

        