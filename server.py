from enlace import *
import time
from comunicador import Comunicador
from arquivo import Arquivo
from datetime import datetime


#arduinoDue
serialName = "COM6"


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        server = Comunicador(serialName, 0 )

        log= open("logservidor.txt","w+")


        print("-------------------------")
        print('Porta Com habilitada')
        print("-------------------------")
        
        hs = False

        serverid = 10
       
        while hs == False:
            server.getHead()
            server.getEop()
            tamanho = len(server.head) + len(server.eop_recebida)
            tipo = str(server.h0)
            escrito = str(datetime.now()) + "/" + "Recebimento"+"/" + tipo + "/"+ str(tamanho) + "\n"
            log.write(escrito)
            if server.h0 == 1 and server.h2 == serverid:
                print(" handshake respondido")
                numPacotes = server.h3
                server.rogerHS()
                log.write(str(datetime.now()) + "/" + "Envio"+"/"+"2" + "/"+ "14"+ "\n")
                hs = True 
    
        doingIt = True

        count = 1


        while count <= numPacotes:
            t1= time.clock()
            t2= time.clock()
            doingIt = True
            while doingIt:
                if not server.com.rx.getIsEmpty():
                    print("m")
                    server.getHead()
                    server.getPayload()
                    server.getEop()
                    tamanho = len(server.head) + len(server.payload) + len(server.eop_recebida)
                    log.write(str(datetime.now()) + "/" + "Recebimento"+"/" +str(server.h0) + "/"+ str(tamanho)+"/"+  str(server.h4)+"/" + str(server.h3)+"/" + str(server.h8h9) + "\n")
                    server.sendAcknowlage()
                    log.write(str(datetime.now()) + "/" + "Envio"+ "/"+ str(server.resp) + "/"+ "14"+ "\n")
                    if server.conferData():
                        print("Pacote recebido com sucesso ", server.lastPackage + 1)
                        server.joinPackages(server.payload)
                        count += 1
                    doingIt = False
                else:
                    if time.clock() - t2 > 20:
                        server.timeOut()
                        log.write(str(datetime.now()) + "/" + "Envio"+"/" +str(server.restm) + "/"+ "14"+ "\n")
                        count = numPacotes + 1
                        doingIt = False
                    if time.clock() - t1 > 5:
                        server.sendAcknowlage()
                        log.write(str(datetime.now()) + "/" + "Envio"+ "/"+ str(server.resp) + "/"+ "14"+ "\n")
                        t1 = time.clock()


        log.close()
            
            


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
