from enlace import *
import time
from comunicador import Comunicador
from arquivo import Arquivo


#arduinoDue
serialName = "COM6"


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        server = Comunicador(serialName)


        print("-------------------------")
        print('Porta Com habilitada')
        print("-------------------------")
        
        hs = False
       
        while hs == False:
            server.getHead()
            server.getEop()
            if server.h0 == 1:
                print(" handshake respondido")
                server.rogerHS()
                hs = True 
    
        doingIt = True

        while doingIt == True:

            server.getHead()


            server.getPayload()
            server.getEop()
            server.sendAcknowlage()
            if server.conferData():
                print("Pacote recebido com sucesso ", server.lastPackage)
                server.joinPackages(server.payload)
                if server.h4 == server.h3:
                    doingIt = False
            
            


        imageW = "./recebidaTeste.png"
        print("-------------------------")
        print ("Salvando dados no arquivo :")
        print (" - {}".format(imageW))
        f = open(imageW, 'wb')
        f.write(server.complete_payload)

        f.close()   

        print("-------------------------")
        print("imagem recebida e salva")
        print("-------------------------")
        print("Comunicação Finalizada")

        server.end()


    except:
        print("ops! :-\\")
        server.end()
        
if __name__ == "__main__":
    main()
