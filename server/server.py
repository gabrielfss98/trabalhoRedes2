import socket
import os
import tqdm
import hashlib

# Função que retorno o nome dos arquivos
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

# Retorna o arquivo selecionado, com base no número de indentificação do arquivo
def return_file(num):
    buffer_size = 100
    path = f'arquivo_{num}.txt'
    filesize = os.path.getsize(path)
    f = path + '~' + str(filesize)   #nome do arquivo e tamanho
    skt.sendto(f.encode(), address)   #envia para o cliente
    print(f'Enviando {path} ...')
    window_size = 10
    packet_list = list()
    packet_n = 0
    with open(path, 'r') as f:
        while True:
            packet_read = f.read(buffer_size)
            bytes_read = packet_read.encode()
            # adiciona o número do pacote 
            segment = str(packet_n) + '/' + packet_read
            # TALVEZ MUDAR PARA NÚMEROS QUE N SE REPETEM
            packet_n += 1
            # salva o pacote na lista
            packet_list.append(segment)
            # janela deslisante
            # caso não existam pacotes verifica se ainda existe algum na lista
            if not packet_read:
                # se a lista estiver vazia finaliza 
                if len(packet_list) == 0:
                    # remove o últmo pacote cirado, ele so contém um número
                    packet_list.pop()
                    # envia mensagem de fim de arquivo
                    skt.sendto(b'end_file', address)
                    break
                else:  # o arquivo acabou, mas ainda há segmentos no buffer
                    packet_list.pop()
                    # envia que resta na lista
                    for i in range(len(packet_list)):
                        skt.sendto(packet_list[i].encode(), address) 
                    skt.sendto(b'end_file', address)
                    ack = skt.recvfrom(1496)[0]
                    ack = ack.decode()
                    check_ack(ack, window_size, address, packet_list, packet_n)
                    break
                
            # quando o tamanho da lista é igual a janela
            if len(packet_list) == window_size:
                # envia todos os pacotes da lista
                for i in range(len(packet_list)):
                    skt.sendto(packet_list[i].encode(), address)   #envia o arquivo em pacotes
                # esperando ACK
                ack = skt.recvfrom(1496)[0]
                ack = ack.decode()
                # se o ack contém um número significa que occoru um erro 
                # reenvia a partir do índice recebido no ack
                check_ack(ack,window_size, address, packet_list, packet_n)
    print('Arquivo enviado !')

# Verifica o ACK emitido pelo cliente
def check_ack(ack, window_size, address,packet_list,packet_n):
    if ack != 'ok':
        index = int(ack)
        #packet_list[index] = '1/oi'
        if len(packet_list) == window_size:
            n = window_size
        else:
            n = len(packet_list)
        for i in range(index, n):
            print(f'Reenviando pacote {i} ...')
            skt.sendto(packet_list[i].encode(), address)
            # lista a lista e zera o contador
        packet_list.clear()
        packet_n = 0 
    else:
        packet_n = 0
        packet_list.clear()


# ---------------------------------- MAIN ------------------------------------------ #

# Busca o ip da maquina cliente para abrir o socket
hostName = socket.gethostname()
ipAddress = socket.gethostbyname(hostName)

# Define o Socket e abre a porta especificada
skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket UDP
server_address = (ipAddress, 1998)   # IP do servidor e porta de comunicação
print(f'IP dos servidor: {server_address[0]}, Porta: {server_address[1]}')
skt.bind(server_address)

# loop do servidor para escutar as requisições
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
        # try:
        return_file(file_number)  #retorna o conteúdo do arquivo
        # except:
            # print('file error')   
    else:
        skt.sendto(b'ACK', address)
        #print(f'ACK enviado para {address}')
        print(data)

    print('\n\n')
