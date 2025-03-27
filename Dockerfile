# Usar imagem base do Python
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar ferramentas de rede
RUN apt-get update && apt-get install -y iputils-ping

# Copiar arquivos necessários
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Definir o comando padrão
CMD ["python", "time_server.py"]