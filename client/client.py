import socket
import sys

class Client:

    def __init__(self, host, port):
        self.server_adress = (host, port)
        self.data = None
        self.server = None
        # criando socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
    # envia o número correspondente ao aqruivo desejado
    def send_data(self, num):
        teste = ''
        try:
            # enviado solicitação
            print(f'Solicitando arquivo {num} ')
            sent = self.socket.sendto(num, self.server_adress)
            # recebendo resposta
            self.data, self.server = self.socket.recvfrom(4096)
            print(f'{self.data}')
        finally:
            self.socket.close()
    
    def see_files(self):
        sent = self.socket.sendto(b'archieves', self.server_adress)
            # recebendo resposta
        self.data, self.server = self.socket.recvfrom(4096)
        print('Arquivos disponíveis para download: ')
        files = str(self.data)
        files = files.replace('b', '')
        files = files.split(' ')
        print(files)

            
c = Client('localhost', 1998)
c.see_files()
#c.send_data(b'archieves')

