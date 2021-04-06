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

def return_file(num):
    path = f'./server/arquivo_{num}.txt'
    with open(path, 'rb') as f:
        contents = f.read()
    print('Enviando arquivo')
    skt.sendto(contents, address)
        
while True:
    print('Aguardando requisições ...')
    data, address = skt.recvfrom(4096)
    print(f'Recebidos {len(data)} bytes de {address}')
    # se a mensagem recebida for 'archieves' mostra os arquivos disponíveis
    if data == b'archieves':
        name_files(address)
        # fica esperando uma resposta
        print('Esperando arquivo ser selecionado...')
        file_name = skt.recvfrom(4096)
        # convertendo bytes para string
        file_name = file_name[0].decode('utf-8')
        print(f'Arquivo selecionado {str(file_name)}')
        # recuperando o arquivo selecionado
        try:
            return_file(file_name)
        except:
            print('file error')   
    else:
        skt.sendto(b'ACK', address)
        print(f'ACK enviado para {address}')

    print('\n\n')
