
---

# Algoritmo de Cristian - Sincronização de Tempo em Sistemas Distribuídos

Este projeto é uma simulação prática do **Algoritmo de Cristian**, utilizado para sincronizar o horário entre um servidor de tempo e múltiplos clientes em um ambiente distribuído. A comunicação entre os nós é feita via **sockets UDP**, e toda a infraestrutura é orquestrada com **Docker Compose**.

## 🧠 Conceito

O **Algoritmo de Cristian** permite que clientes sincronizem seus relógios consultando um servidor de tempo confiável. Neste projeto, o servidor recebe requisições dos clientes e responde com a hora ajustada, considerando o atraso estimado da comunicação entre os nós.

Além disso, o projeto está preparado para utilizar o **protocolo NTP (Network Time Protocol)** por meio da biblioteca `ntplib`, que pode ser facilmente integrada para fornecer uma fonte de tempo mais precisa, caso desejado.

## 📁 Estrutura do Projeto

```
.
├── client.py              # Cliente UDP que solicita a hora periodicamente
├── time_server.py         # Servidor UDP que fornece a hora ajustada
├── Dockerfile             # Imagem base comum para cliente e servidor
├── docker-compose.yml     # Orquestra 1 servidor e 4 clientes
├── requirements.txt       # Lista de dependências (inclui ntplib)
└── README.md              # Documentação do projeto
```

## 🚀 Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Passos

1. **Build e execução dos containers**

```bash
docker-compose up --build
```

2. **Verifique os logs**

Você verá mensagens como:

```
time_server  | Servidor de tempo iniciado em 0.0.0.0:12345
client1      | Requisitando hora ao servidor time_server:12345
client1      | Hora recebida: Thu Mar 27 20:35:42 2025
```

## ⚙️ Funcionamento

- O **servidor** (`time_server.py`) escuta requisições de horário na porta `12345`.
- Quando um cliente envia `TIME_REQUEST`, o servidor calcula o atraso estimado e responde com a hora ajustada.
- Cada **cliente** (`client.py`) envia requisições a cada 10 segundos.

## 🐳 docker-compose.yml

Define os seguintes serviços:

- `time_server`: servidor de tempo
- `client1`, `client2`, `client3`, `client4`: clientes independentes que consultam o servidor

Todos os serviços utilizam a mesma imagem Docker, definida no `Dockerfile`.

## 📦 Requisitos

- Python 3.10+
- `ntplib==0.4.0`  
  > Utilizado para integração com servidores NTP. Embora não esteja ativo por padrão no algoritmo de Cristian, a biblioteca está disponível para possíveis extensões e experimentações com NTP.

## 📖 Referências

- Cristian, F. "Probabilistic clock synchronization", *Distributed Computing*, 1989.
- Comunicação via sockets UDP com o módulo `socket` do Python.
- Documentação oficial do protocolo NTP.

## 📌 Observações

- O tempo ajustado pelo algoritmo considera apenas o tempo de ida da mensagem (sem confirmação de volta), o que pode introduzir pequenas imprecisões.
- O projeto pode ser estendido para:
  - Suporte a múltiplos servidores de tempo;
  - Simulação de latências variáveis;
  - Sincronização direta com servidores NTP reais usando `ntplib`.

## 👨‍💻 Autor

Projeto desenvolvido com fins educacionais e experimentação em disciplinas de **Sistemas Distribuídos**.

---
