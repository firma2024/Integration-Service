# Utiliza una imagen de Java como base para compilar
FROM maven:latest AS build

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Compila tu aplicación Java usando Maven
RUN mvn clean install

# Utiliza una imagen de Java como base para la ejecución
FROM openjdk:8-jdk-alpine
ARG GECKO_DRIVER_VERSION="v0.30.0"
ARG GECKO_DRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_DRIVER_VERSION}/geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz"

# Descarga y descomprime el controlador de GeckoDriver
RUN apk --no-cache add curl tar \
    && curl -SL ${GECKO_DRIVER_URL} | tar -xz -C /usr/local/bin/
# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos generados (incluyendo el .jar) desde la imagen anterior al contenedor final
COPY --from=build /app/target/integracion-0.0.1-SNAPSHOT.jar /app
# Define el comando a ejecutar cuando se inicie el contenedor
CMD ["java", "-jar", "integracion-0.0.1-SNAPSHOT.jar"]