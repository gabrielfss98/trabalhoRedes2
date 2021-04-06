import socket
import sys

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
        print('Digite o número do arquivo')
        file_name = str(input())
        try:
            # enviado solicitação
            print(f'Solicitando arquivo {file_name} ')
            sent = self.socket.sendto(file_name.encode(), self.server_adress)
            # recebendo resposta
            self.file, self.server = self.socket.recvfrom(4096)
            self.file = self.file.decode('utf-8')
            print(f'{self.file}')
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

