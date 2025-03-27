import socket
import time
import logging
import ntplib

# Configurações de logging
# O nível de logging é definido como INFO, o que significa que mensagens de nível INFO e superiores (WARNING, ERROR, etc.) serão exibidas.
logging.basicConfig(level=logging.INFO)

def start_server(host='0.0.0.0', port=12345):
    # Esta função inicia um servidor UDP que escuta requisições de hora.
    # O host padrão '0.0.0.0' permite que o servidor escute em todas as interfaces de rede disponíveis.
    # A porta padrão é 12345, que é a porta na qual o servidor irá escutar as requisições.

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Cria um socket UDP (AF_INET indica que estamos usando IPv4 e SOCK_DGRAM indica que é um socket UDP).
        # O contexto 'with' garante que o socket será fechado corretamente após o uso.
        
        server_socket.bind((host, port))
        # O método bind associa o socket ao endereço IP e à porta especificados, permitindo que ele receba mensagens nesse endereço.

        logging.info(f"Servidor de tempo iniciado em {host}:{port}")
        # Registra uma mensagem de informação indicando que o servidor foi iniciado e está pronto para receber requisições.

        while True:
            # Um loop infinito que mantém o servidor em execução, aguardando requisições.
            data, addr = server_socket.recvfrom(1024)
            # O método recvfrom bloqueia a execução até que uma mensagem seja recebida.
            # Recebe até 1024 bytes de dados e o endereço do cliente que enviou a requisição.

            if data.decode() == "TIME_REQUEST":
                # Verifica se a mensagem recebida é uma requisição de hora.
                logging.info(f"Requisição de hora recebida de {addr}")

                # Obtém a hora correta usando o ntplib
                try:
                    client = ntplib.NTPClient()
                    response = client.request('pool.ntp.org')  # Faz uma requisição a um servidor NTP
                    adjusted_time = response.tx_time  # O tempo transmitido pelo servidor NTP
                    response_time = time.ctime(adjusted_time)  # Converte o tempo transmitido em uma string legível
                except Exception as e:
                    logging.error(f"Erro ao obter a hora do servidor NTP: {e}")
                    response_time = "Erro ao obter a hora"

                # Envia a resposta de volta ao cliente que fez a requisição
                server_socket.sendto(response_time.encode(), addr)
                logging.info(f"Hora enviada para {addr}: {response_time}")

if __name__ == "__main__":
    start_server()
    # Verifica se o script está sendo executado diretamente (não importado como um módulo) e chama a função start_server para iniciar o servidor.
