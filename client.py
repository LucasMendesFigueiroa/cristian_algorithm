import socket
import time
import logging

# Configurações de logging
# O nível de logging é definido como INFO, o que significa que mensagens de nível INFO e superiores (WARNING, ERROR, etc.) serão exibidas.
logging.basicConfig(level=logging.INFO)

def request_time(server_ip, server_port):
    # Esta função é responsável por solicitar a hora ao servidor especificado.
    # Recebe o endereço IP e a porta do servidor como parâmetros.

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        # Cria um socket UDP (AF_INET indica que estamos usando IPv4 e SOCK_DGRAM indica que é um socket UDP).
        # O contexto 'with' garante que o socket será fechado corretamente após o uso.

        sock.settimeout(1)  # Define um tempo de espera de 1 segundo para receber uma resposta.
        
        try:
            # Enviar requisição de hora
            logging.info(f"Requisitando hora ao servidor {server_ip}:{server_port}")
            # Registra uma mensagem de informação indicando que está fazendo a requisição de hora ao servidor.

            sock.sendto(b"TIME_REQUEST", (server_ip, server_port))
            # Envia uma mensagem "TIME_REQUEST" para o servidor no endereço IP e na porta especificados.
            # A mensagem é codificada em bytes.

            # Receber resposta
            data, _ = sock.recvfrom(1024)
            # O método recvfrom bloqueia a execução até que uma mensagem seja recebida.
            # Recebe até 1024 bytes de dados e descarta o endereço do remetente.

            logging.info(f"Hora recebida: {data.decode()}")
            # Decodifica a resposta recebida de bytes para string e registra uma mensagem de informação com a hora recebida.
        
        except socket.timeout:
            logging.error("Tempo de espera esgotado, servidor não respondeu.")
            # Se o tempo de espera expirar sem receber resposta, registra uma mensagem de erro.
        
        except Exception as e:
            logging.error(f"Erro ao requisitar hora: {e}")
            # Captura quaisquer outras exceções que possam ocorrer durante a requisição e registra uma mensagem de erro com detalhes.

if __name__ == "__main__":
    SERVER_IP = "time_server"  # Nome do serviço no Docker Compose
    SERVER_PORT = 12345  # Porta do servidor
    while True:
        request_time(SERVER_IP, SERVER_PORT)
        # Chama a função request_time repetidamente para requisitar a hora do servidor.
        
        time.sleep(10)  # Intervalo de requisição de 10 segundos entre as solicitações.