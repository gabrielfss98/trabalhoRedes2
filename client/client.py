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
            with open(file_name, "w") as f:
                while True:
                    segment, add = self.socket.recvfrom(1460)  #recebe o arquivo em pacotes
                    segment = segment.decode('utf-8')
                    if '/' in segment:        #segmento padrão
                        cheksum_server = segment.split('/')[0]
                        data_read = segment.split('/')[1]
                        cheksum_client = sum(data_read.encode())
                        if cheksum_client != int(cheksum_server):
                            print('ERRO DE BIT !!')
                    else:                      #mensagem de fim de arquivo
                        data_read = segment
                    if data_read == 'end_file':
                        break
                    progress.update(len(data_read.encode()))
                    f.write(data_read)

        finally:
            self.socket.close()
    
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

