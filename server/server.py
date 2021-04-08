import socket
import os
import tqdm

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
    f = path + '~' + str(filesize)
    skt.sendto(f.encode(), address)
    progress = tqdm.tqdm(range(filesize), f"Sending {path}", unit="B", unit_scale=True, unit_divisor=1024, colour='green')
    
    with open(path, 'rb') as f:
        while True:
            bytes_read = f.read(buffer_size)
            progress.update(len(bytes_read))
            if not bytes_read:
                skt.sendto(b'end_file', address)
                # file transmitting is done
                break
        # we use sendall to assure transimission in 
        # busy networks
            skt.sendto(bytes_read, address)
            # update the progress bar
        #contents = f.read()
    #file_name_content = path + '~' + contents
    #print(f'Enviando arquivo {num} ...')
    #skt.sendto(file_name_content.encode(), address)
    print('Arquivo enviado !')
        
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
        # recuperando o arquivo selecionado
        #try:
        return_file(file_name)
        #except:
            #print('file error')   
    else:
        skt.sendto(b'ACK', address)
        print(f'ACK enviado para {address}')

    print('\n\n')
