import socket
import time
import logging
import random

# Configurações de logging
logging.basicConfig(level=logging.INFO)

class InternalClock:
    def __init__(self):
        self.current_time = None  # Armazena a hora atual do relógio interno
        self.last_sync_time = None  # Armazena a última hora sincronizada
        self.offset = 0  # Atraso acumulado

    def sync(self, server_time):
        # Sincroniza o relógio interno com o tempo do servidor
        self.current_time = server_time
        self.last_sync_time = time.time()  # Armazena o tempo da sincronização

    def update(self):
        # Atualiza o relógio interno com base no tempo decorrido
        if self.last_sync_time is not None:
            elapsed_time = time.time() - self.last_sync_time  # Tempo decorrido desde a última sincronização
            
            # Adiciona um atraso aleatório entre 0 e 5 segundos
            random_delay = random.uniform(0, 5)  # Gera um atraso aleatório entre 0 e 5 segundos
            self.offset += elapsed_time + random_delay  # Atualiza o atraso acumulado
            self.current_time += elapsed_time + random_delay  # Avança o relógio interno
            self.last_sync_time = time.time()  # Atualiza o tempo da última sincronização

    def get_time(self):
        # Retorna o tempo atual do relógio interno
        if self.current_time is None:
            return None
        return time.ctime(self.current_time + self.offset)  # Adiciona o atraso acumulado

def request_time(server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(1)  # Define um tempo de espera de 1 segundo para receber uma resposta.
        
        try:
            logging.info(f"Requisitando hora ao servidor {server_ip}:{server_port}")
            sock.sendto(b"TIME_REQUEST", (server_ip, server_port))
            data, _ = sock.recvfrom(1024)
            current_time = float(data.decode())  # Armazena a hora recebida em uma variável
            logging.info(f"Hora recebida: {current_time}")
            return current_time  # Retorna a hora recebida
        
        except socket.timeout:
            logging.error("Tempo de espera esgotado, servidor não respondeu.")
            return None
        
        except Exception as e:
            logging.error(f"Erro ao requisitar hora: {e}")
            return None

if __name__ == "__main__":
    SERVER_IP = "time_server"  # Nome do serviço no Docker Compose
    SERVER_PORT = 12345  # Porta do servidor

    clock = InternalClock()  # Cria uma instância do relógio interno

    while True:
        # Atualiza o relógio interno
        clock.update()

        # Requisita a hora ao servidor
        server_time = request_time(SERVER_IP, SERVER_PORT)
        
        if server_time is not None:
            clock.sync(server_time)  # Sincroniza o relógio interno com a hora do servidor
        
        # Obtém a hora atual do relógio interno
        internal_time = clock.get_time()  
        if internal_time:
            print(f"Hora atual do relógio interno: {internal_time}")  # Exibe a hora recebida
        
        time.sleep(10)  # Intervalo de requisição de 10 segundos entre as solicitações.
