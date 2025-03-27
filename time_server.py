import socket
import logging
import ntplib

# Configurações de logging
logging.basicConfig(level=logging.INFO)

def start_server(host='0.0.0.0', port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        logging.info(f"Servidor de tempo iniciado em {host}:{port}")

        while True:
            data, addr = server_socket.recvfrom(1024)
            if data.decode() == "TIME_REQUEST":
                logging.info(f"Requisição de hora recebida de {addr}")

                # Obtém a hora correta usando o ntplib
                try:
                    client = ntplib.NTPClient()
                    response = client.request('pool.ntp.org')  # Faz uma requisição a um servidor NTP
                    adjusted_time = response.tx_time  # O tempo transmitido pelo servidor NTP
                except Exception as e:
                    logging.error(f"Erro ao obter a hora do servidor NTP: {e}")
                    adjusted_time = time.time()  # Se falhar, usa o tempo local

                # Envia a resposta de volta ao cliente que fez a requisição como um float
                server_socket.sendto(str(adjusted_time).encode(), addr)
                logging.info(f"Hora enviada para {addr}: {adjusted_time}")

if __name__ == "__main__":
    start_server()
