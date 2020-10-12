
from enlace import *
import time
from comunicador import Comunicador
from arquivo import Arquivo
from datetime import datetime

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
# para saber a sua porta, execute no terminal :
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)


# se fosse apenas o arduino, uma porta de comunicaçã seria suficiente, estamos usando duas pq o software de emular recebe um uma porta e envia em outra
# serialName1 = "COM1"
# serialName2 = "COM2"                 # Windows(variacao de)


#Uno
serialName = "COM7"


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.

        imagem = "./imageB.png"
        data = Arquivo(imagem)
        dividedPackages = data.setPacotes()



        client = Comunicador(serialName,data.total_payloads)


        log= open("logclient.txt","w+")




        print("-------------------------")
        print("Checking server avalability")
        print("-------------------------")



        doingIt = True
        onlineCheck = True
        while onlineCheck == True:
            client.sendHS(45)
            log.write(str(datetime.now()) + "/" + "Envio"+"/"+"1" + "/"+ "14"+ "\n")
            time.sleep(3)
            if client.com.rx.getIsEmpty() == True:
                x = input("Sem resposta. Enviar Novamente (Y/N)")
                if x == "N":
                    onlineCheck = False
            else:
                client.getHead()
                client.getEop()
                tamanho = len(client.head) + len(client.eop_recebida)
                tipo = str(client.h0)
                escrito = str(datetime.now()) + "/" + "Recebimento"+"/" + tipo + "/"+ str(tamanho) + "\n"
                log.write(escrito)
                if client.h0 == 2:
                    onlineCheck = True
                    indexPackageToBeSent = 0

                    while(indexPackageToBeSent < data.total_payloads ):
                        t1= time.clock()
                        t2= time.clock()
                        doingIt = True
                        
                        client.sendPackage(dividedPackages[indexPackageToBeSent])
                        while doingIt:
                            if not client.com.rx.getIsEmpty():
                                linha = str(datetime.now()) + "/" + "Envio"+"/"+ str(dividedPackages[indexPackageToBeSent][0]) + "/"+ str(len(dividedPackages[indexPackageToBeSent])) + "/" + str(indexPackageToBeSent + 1) + "/" +  str(data.total_payloads) + "/" + str(dividedPackages[indexPackageToBeSent][8:10]) + "\n"
                                log.write(linha)
                                client.getHead()
                                client.getEop()
                                print(client.h0)
                                log.write(str(datetime.now()) + "/" + "Recebimento"+"/" +str(client.h0) + "/"+ "14"+ "\n")
                                if client.h0== 6:
                                    indexPackageToBeSent = client.h6 - 1
                                    print("-------------------------")
                                    print("Erro no", client.h6)
                                    print("Enviando novamente")
                                    print("-------------------------")
                                else:
                                    print("Pacote {} de {}  enviado".format(indexPackageToBeSent + 1, data.total_payloads))
                                    indexPackageToBeSent += 1
                                doingIt = False
                            else:
                                if time.clock() - t2 > 20:
                                    client.timeOut()
                                    log.write(str(datetime.now()) + "/" + "Envio"+"/" +str(client.restm) + "/"+ "14"+ "\n")
                                    doingIt = False
                                    indexPackageToBeSent = data.total_payloads
                                if time.clock() - t1 > 5:
                                    client.sendPackage(dividedPackages[indexPackageToBeSent])
                                    linha = str(datetime.now()) + "/" + "Envio"+"/"+ str(dividedPackages[indexPackageToBeSent][0]) + "/"+ str(len(dividedPackages[indexPackageToBeSent])) + "/" + str(indexPackageToBeSent + 1) + "/" +  str(data.total_payloads) + "/" + str(dividedPackages[indexPackageToBeSent][8:10]) + "\n"
                                    log.write(linha)
                                    t1 = time.clock()



                    log.close()
                    onlineCheck = False
                    

            
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação Finalizada")
        print("-------------------------")
        client.end()
    except:
        print("ops! :-\\")
        client.com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
