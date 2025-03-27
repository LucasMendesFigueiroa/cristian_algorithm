import socket
import time
import logging

# Configurações de logging
# O nível de logging é definido como INFO, o que significa que mensagens de nível INFO e superiores (WARNING, ERROR, etc.) serão exibidas.
logging.basicConfig(level=logging.INFO)

def calculate_time_delay(receive_time):
    # Esta função calcula o atraso estimado na comunicação.
    # A função recebe o tempo em que a requisição foi recebida (receive_time).
    # Para simplificação, não está calculando o atraso real da rede (que envolveria medir o tempo de ida e volta da mensagem).
    return (time.time() - receive_time) / 2  # Retorna o atraso estimado como a metade do tempo decorrido.

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
                receive_time = time.time()
                # Registra o tempo em que a requisição foi recebida.

                delay = calculate_time_delay(receive_time)
                # Chama a função calculate_time_delay para estimar o atraso e armazena o resultado na variável delay.

                adjusted_time = receive_time + delay
                # Ajusta a hora recebida somando o atraso estimado.

                response = f"{time.ctime(adjusted_time)}"
                # Converte o tempo ajustado em uma string legível (formato de data e hora) para a resposta.

                server_socket.sendto(response.encode(), addr)
                # Envia a resposta de volta ao cliente que fez a requisição, codificando a string em bytes.

                logging.info(f"Hora enviada para {addr}: {response}")
                # Registra uma mensagem de informação indicando que a hora foi enviada para o cliente, incluindo o endereço do cliente e a hora enviada.

if __name__ == "__main__":
    start_server()
    # Verifica se o script está sendo executado diretamente (não importado como um módulo) e chama a função start_server para iniciar o servidor.