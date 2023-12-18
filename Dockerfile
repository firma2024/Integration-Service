# Utiliza una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo
WORKDIR app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean
EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port $PORT