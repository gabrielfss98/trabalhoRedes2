import socket

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP
server_address = ('localhost', 1998)   # IP do servidor e porta de comunicação
print(f'IP dos servidor: {server_address[0]}, Porta: {server_address[1]}')
skt.bind(server_address)


while True:
    print('Aguardando requisições ...')
    data, address = skt.recvfrom(4096)
    print(f'Recebidos {len(data)} bytes de {address}')
    skt.sendto(b'ACK', address)
    print(f'ACK enviado para {address}')
    print('\n\n')
