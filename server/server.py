import socket

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP
server_address = ('localhost', 1998)   # IP do servidor e porta de comunicação
print(f'IP dos servidor: {server_address[0]}, Porta: {server_address[1]}')
skt.bind(server_address)


def name_files(address):
    name = ''
    for i in range(5):
        k = str(i+1)
        name = name +  f'arquivo_{k}.txt' + ' '
    skt.sendto(name.encode(), address)
        
        


while True:
    print('Aguardando requisições ...')
    data, address = skt.recvfrom(4096)
    print(f'Recebidos {len(data)} bytes de {address}')
    if data == b'archieves':
        name_files(address)
    else:
        skt.sendto(b'ACK', address)
        print(f'ACK enviado para {address}')

    print('\n\n')
