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
            print(f'{self.data} recebidos ')
        finally:
            self.socket.close()
            
c = Client('localhost', 1998)
c.send_data(b'thanks')

