import socket

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #Socket UDP
server_address = ('localhost', 1998)     #Ip do servidor
skt.sendto(b'archives', server_address)
message = b'getArquivo'
try:
    print(f'Enviando mensagem: {message}')
    skt.sendto(message, server_address)
    print('Aguardando resposta ...')
    data, server = skt.recvfrom(4096)
    print(f'Recebido: {data}')
finally:
    skt.close()

