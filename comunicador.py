from enlace import *
import time

class Comunicador(object):
    def __init__(self, serialName):
        self.serialName = serialName
        self.com = enlace(serialName)
        self.com.enable()
        self.eop = b""
        self.complete_payload = b""
        self.lastPackage = 0
        self.eop = (255).to_bytes(1, byteorder="big") + (170).to_bytes(1, byteorder="big") + (255).to_bytes(1, byteorder="big") + (170).to_bytes(1, byteorder="big")
        self.sensorId = (8).to_bytes(1, byteorder="big")
        self.serverId = (10).to_bytes(1, byteorder="big")

    def getHead(self):
        self.head, r = self.com.getData(10)


        # self.message_type = self.head[0]
        # self.hs_response = self.head[1]
        # self.error_package = self.head[2]
        # self.nPackage = self.head[3]
        # self.package_index = self.head[4]
        # self.payload_size = self.head[5]
        # self.acknolage_confirmartion = self.head[6]

        self.h0 = self.head[0]
        self.h1 = self.head[1]
        self.h2 = self.head[2]
        self.h3 = self.head[3]
        self.h4 = self.head[4]
        self.h5 = self.head[5]
        self.h6 = self.head[6]
        self.h7 = self.head[7]
        self.h8 = self.head[8]
        self.h9 = self.head[9]

    def getPayload(self):
        self.payload, teste = self.com.getData(self.h5)

    def getEop(self):
        self.eop_recebida, vau= self.com.getData(4)

    def conferData(self):

        # Falta conferir o CRC
        if self.h5 == len(self.payload) and self.eop_recebida == self.eop and self.h4 == self.lastPackage + 1:
            return True
        else:
            return False

    def sendAcknowlage(self):
        head = b""
        pacote = b""
        h1 = (0).to_bytes(1, byteorder="big")
        h2 = (0).to_bytes(1, byteorder="big")
        h3 = (0).to_bytes(1, byteorder="big")
        h4 = (0).to_bytes(1, byteorder="big")
        h5 = (0).to_bytes(1, byteorder="big")
        h8 = (0).to_bytes(1, byteorder="big")
        h9 = (0).to_bytes(1, byteorder="big")


        # h0 = (1).to_bytes(1, byteorder="big")
        # h6 = (0).to_bytes(1, byteorder="big")
        # h7 = (0).to_bytes(1, byteorder="big")


        if self.conferData() == False:
            
            h0 = (6).to_bytes(1, byteorder="big")
            h6 = (self.h4).to_bytes(1, byteorder="big")
            h7 = (0).to_bytes(1, byteorder="big")
            print("-------------------")
            print("O pacote {} esta corrompido".format(self.lastPackage + 1))
            print("Pedindo o reenvio do pacote")
            self.com.rx.clearBuffer()
        else:
            h0 = (4).to_bytes(1, byteorder="big")
            h6 = (0).to_bytes(1, byteorder="big")
            h7 = (self.h4).to_bytes(1, byteorder="big")
            
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9
        pacote = head + self.eop
        self.com.sendData(pacote)
        time.sleep(0.5)

    def sendHS(self, idArquivo):
        head = b""
        pacote = b""
        print("entrou hs-------")
        h0 = (1).to_bytes(1, byteorder="big")
        h1 = self.sensorId
        h2 = self.serverId
        h3 = (0).to_bytes(1, byteorder="big")
        h4 = (0).to_bytes(1, byteorder="big")
        h5 = (idArquivo).to_bytes(1, byteorder="big")
        h6 = (0).to_bytes(1, byteorder="big")
        h7 = (0).to_bytes(1, byteorder="big")
        h8 = (0).to_bytes(1, byteorder="big")
        h9 = (0).to_bytes(1, byteorder="big")
        head = h0 + h1 + h2 + h3 + h4  + h5 + h6 + h7 + h8 + h9
        pacote = head + self.eop
        print("entrou hs")
        self.com.sendData(pacote)
        time.sleep(0.5)

    def rogerHS(self):
        head = b""
        pacote = b""
        h0 = (2).to_bytes(1, byteorder="big")
        h1 = (0).to_bytes(1, byteorder="big")
        h2 = (0).to_bytes(1, byteorder="big")
        h3 = (0).to_bytes(1, byteorder="big")
        h4 = (0).to_bytes(1, byteorder="big")
        h5 = (0).to_bytes(1, byteorder="big")
        h6 = (0).to_bytes(1, byteorder="big")
        h7 = (0).to_bytes(1, byteorder="big")
        h8 = (0).to_bytes(1, byteorder="big")
        h9 = (0).to_bytes(1, byteorder="big")
        head = h0 + h1 + h2 + h3 + h4 + h4 + h5 + h6 + h7 + h8 + h9
        pacote = head + self.eop
        self.com.sendData(pacote)
        time.sleep(0.5)

    def timeOut(self):
        head = b""
        pacote = b""
        h0 = (5).to_bytes(1, byteorder="big")
        h1 = (0).to_bytes(1, byteorder="big")
        h2 = (0).to_bytes(1, byteorder="big")
        h3 = (0).to_bytes(1, byteorder="big")
        h4 = (0).to_bytes(1, byteorder="big")
        h5 = (0).to_bytes(1, byteorder="big")
        h6 = (0).to_bytes(1, byteorder="big")
        h7 = (0).to_bytes(1, byteorder="big")
        h8 = (0).to_bytes(1, byteorder="big")
        h9 = (0).to_bytes(1, byteorder="big")
        head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h7 + h8 + h9
        pacote = head + self.eop
        self.com.sendData(pacote)
        time.sleep(0.5)

    def end(self):
        self.com.disable()

    def sendPackage(self, x):
        self.com.sendData(x)
        time.sleep(0.5)

    def joinPackages(self, payload):
        self.lastPackage +=1 
        self.complete_payload += payload

        
        
