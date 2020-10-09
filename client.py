
from enlace import *
import time
from comunicador import Comunicador
from arquivo import Arquivo

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

        #imagem = input("Coloque o endereço da imagem que deseja enviar: ")



        # print("-------------------------")
        # print("TESTANDO ERRO NO TAMANHO DO PAYLOAD")
        # print("-------------------------")





        print("-------------------------")
        print("Checking server avalability")
        print("-------------------------")




        onlineCheck = True
        while onlineCheck == True:
            client.sendHS(45)
            time.sleep(3)
            if client.com.rx.getIsEmpty() == True:
                x = input("Sem resposta. Enviar Novamente (Y/N)")
                if x == "N":
                    onlineCheck = False
            else:
                client.getHead()
                client.getEop()
                if client.h0 == 2:
                    onlineCheck = True
                    
                    # Log
                    print("Comunicação inicializada")
                    print("-------------------------")

                    print("-------------------------")
                    print ("Carregando imagem para transmissão :")
                    print("-------------------------")
                    
                    
                    print("-------------------------")
                    print ("Imagem Pronta para ser enviada:")
                    print("-------------------------")

                    indexPackageToBeSent = 0

                    while(indexPackageToBeSent < data.total_payloads ):
                        t1= time.clock()
                        t2= time.clock()
                        client.sendPackage(dividedPackages[indexPackageToBeSent])
                        client.getHead()
                        client.getEop()
                        if client.h0== 6:
                            indexPackageToBeSent = client.h6 - 1 
                            print("-------------------------")
                            print("Erro no", indexPackageToBeSent)
                            print("Enviando novamente")
                            print("-------------------------")
                        else:
                            print("Pacote {} de {}  enviado".format(indexPackageToBeSent + 1, data.total_payloads))
                            indexPackageToBeSent += 1
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
