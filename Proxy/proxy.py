import threading
import socket

def handler_doNothing(txt):
        return txt

class proxy:
    def __init__(self, serverIp, serverPort, clientPort, clientManipulation=handler_doNothing, serverManipulation=handler_doNothing):
        self.serverIp           = serverIp
        self.serverPort         = serverPort
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

        for x in self.threads:
            x.join()

    def stop(self):
        for x in self.threads:
            x.stop()
        
        self.listenSock.close()
        self.clientSock.close()
        self.serverSock.close()

        