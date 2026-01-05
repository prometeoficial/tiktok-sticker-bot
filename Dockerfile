FROM python:3.10-slim

# Instalamos FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# El bot corre en el puerto 8080 para que el servidor lo vea vivo
EXPOSE 8080
CMD ["python", "main.py"]
