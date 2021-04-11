import socket
import sys
import tqdm

class Client:

    def __init__(self, host, port):
        self.server_adress = (host, port)
        self.data = None
        self.server = None
        self.file = None
        # criando socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
    # envia o número correspondente ao aqruivo desejado
    def request_file(self):
        buffer_size = 15
        print('Digite o número do arquivo')
        file_number = str(input())
        try:
            # enviado solicitação (número do arquivo)
            print(f'Solicitando arquivo {file_number} ')
            sent = self.socket.sendto(file_number.encode(), self.server_adress)
            # recebendo resposta (nome e tamanho do arquivo)
            self.file, self.server = self.socket.recvfrom(4096) #resposta do servidor
            self.file = self.file.decode('utf-8')
            file_name = self.file.split('~')[0]    #nome do arquivo
            filesize = int(self.file.split('~')[1])   #tamanho do arquivo

            progress = tqdm.tqdm(range(filesize), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024, colour='green')
            # variáveis para guardar os pacotes
            packet_number = list()
            packet_list = list()
            # tamanho da janela
            window_size = 10
            with open(file_name, "w") as f:
                while True:
                    segment, add = self.socket.recvfrom(1460)  #recebe o arquivo em pacotes
                    segment = segment.decode('utf-8')
                    # se o segmento recebido é de final de arquivo 
                    if segment == 'end_file':
                        # se existe alguma coisa na lista escreve
                        if len(packet_list) > 0:
                            for i in packet_list:
                                k = f.write(i)
                                progress.update(k)
                        break
                    # salva o pacote e o número de listas
                    packet_number.append(int(segment.split('/')[0])) 
                    packet_list.append(segment.split('/')[1])
                    # quando uma janela completa é recebida
                    if len(packet_list) == window_size:
                        # verifica se existem pacotes faltando
                        ack = self.check_ack(packet_number)
                        if ack != 'ok':
                            ack = str(ack)
                            # manda o índice do pacote errado
                            self.socket.sendto(ack.encode(), self.server_adress)
                            # elimina todos os pacotes a partir do primeiro errado
                            ack = int(ack)
                            packet_list = packet_list[:ack]
                            # recupera os números dos pacotes certos
                            # TEM QUE MUDAR, CASO OS NÚMEROS NÃO SEJAM SO DE 0 A 9
                            packet_number.clear()
                            for i in range(len(packet_list)):
                                packet_number.append(i)
                            
                            for i in range(window_size - ack):
                                packet = self.socket.recvfrom(1460)[0]
                                number = packet.decode('utf-8').split('/')[0]
                                packet_number.append(number)
                                packet = packet.decode('utf-8').split('/')[1]
                                packet_list.append(packet)
                            
                            for i in packet_list:
                                a = f.write(i)
                                progress.update(a)
                            # limpa as listas para a proxima janela
                            packet_list.clear()
                            packet_number.clear() 


                            
                        else:
                            # caso não existe erro, escreve os pacotes no arquivo   
                            for i in packet_list:
                                a = f.write(i)
                                progress.update(a)
                            # limpa as listas para a proxima janela
                            packet_list.clear()
                            packet_number.clear() 
                        # envia ack 'ok'  
                                 
        finally:
            self.socket.close()
    
    def check_ack(self, packet_number):
        for i in range(len(packet_number)- 1):
            if packet_number[i + 1] != packet_number[i] + 1:
                #print('erro no pacote da posição ', i+1)
                return i + 1
        return 'ok'
    
    def see_files(self):
        try:
            sent = self.socket.sendto(b'archieves', self.server_adress)
            # recebendo resposta
            self.data, self.server = self.socket.recvfrom(4096)
            print('Arquivos disponíveis para download: ')
            # convertendo bytes para txt
            files = self.data.decode('utf-8').split(' ')
            # imprimindo o nome dos arquivos 
            for i in files:
                print(i)
        except :
            print('erro see_files')
            
c = Client('localhost', 1998)
c.see_files()
c.request_file()
#c.send_data(b'archieves')