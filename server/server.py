import socket
import os
import tqdm
import hashlib

skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP
server_address = ('localhost', 1998)   # IP do servidor e porta de comunicação
print(f'IP dos servidor: {server_address[0]}, Porta: {server_address[1]}')
skt.bind(server_address)


def name_files(address):
    files = os.listdir() # todos os arquivos no diretório
    names = []
    for file in files:
        if '.txt' in file:
            names.append(file)

    name = ''
    for n in names:
        name = name + n + ' '
    
    skt.sendto(name.encode(), address)

def return_file(num):
    buffer_size = 8
    path = f'arquivo_{num}.txt'
    filesize = os.path.getsize(path)
    f = path + '~' + str(filesize)   #nome do arquivo e tamanho
    skt.sendto(f.encode(), address)   #envia para o cliente
    print(f'Enviando {path} ...')
    #progress = tqdm.tqdm(range(filesize), f"Sending {path}", unit="B", unit_scale=True, unit_divisor=1024, colour='green')
    
    with open(path, 'r') as f:
        while True:
            packet_read = f.read(buffer_size)
            bytes_read = packet_read.encode()
            cheksum = sum(bytes_read)
            segment = str(cheksum) + '/' + packet_read
            if not bytes_read:
                skt.sendto(b'end_file', address)  #mensagem de fim de arquivo
                break
            
            skt.sendto(segment.encode(), address)   #envia o arquivo em pacotes
            #progress.update(len(bytes_read))
    print('Arquivo enviado !')
        
while True:
    print('Aguardando requisições ...')
    data, address = skt.recvfrom(4096)
    
    print(f'Recebidos {len(data)} bytes de {address}')
    # se a mensagem recebida for 'archieves' mostra os arquivos disponíveis
    if data == b'archieves':
        name_files(address)  #mostra os arquivos para o cliente
        print('Esperando arquivo ser selecionado...')
        file_number = skt.recvfrom(4096)
        # convertendo bytes para string
        file_number = file_number[0].decode('utf-8')
        # recuperando o arquivo selecionado
        try:
            return_file(file_number)  #retorna o conteúdo do arquivo
        except:
            print('file error')   
    else:
        skt.sendto(b'ACK', address)
        print(f'ACK enviado para {address}')

    print('\n\n')
