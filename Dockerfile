FROM python:3.11-slim

WORKDIR /app
COPY . /app

# Atualizar pip
RUN pip install --upgrade pip

# Copiar o arquivo requirements.txt
COPY requirements.txt .

# Instalar pacotes sem interação e com saída mínima
RUN pip install --quiet -r requirements.txt

# Alterar permissões do entrypoint.sh para garantir que seja executável
RUN chmod +x ./entrypoint.sh
EXPOSE 8000
CMD ["uvicorn", "--host", "0.0.0.0", "meu_projeto_chat.app:app"]
