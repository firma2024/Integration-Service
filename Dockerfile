# Etapa 1: Utiliza una imagen base de Maven para compilar el proyecto
FROM maven:3.8.4-openjdk-8 AS build
WORKDIR /app

# Copia el archivo pom.xml y descarga las dependencias
COPY pom.xml .
RUN mvn dependency:go-offline

# Copia los archivos fuente y compila la aplicación
COPY src src
RUN mvn clean package

# Etapa 2: Utiliza una imagen base de OpenJDK para Java 8
FROM openjdk:8-jdk-alpine

# Define la ubicación del controlador de GeckoDriver
ARG GECKO_DRIVER_VERSION="v0.30.0"
ARG GECKO_DRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_DRIVER_VERSION}/geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz"

# Descarga y descomprime el controlador de GeckoDriver
RUN apk --no-cache add curl tar \
    && curl -SL ${GECKO_DRIVER_URL} | tar -xz -C /usr/local/bin/

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el JAR generado desde la etapa de compilación con el nombre "app.jar"
COPY --from=build /app/target/integracion-0.0.1-SNAPSHOT.jar /app/app.jar

# Expone el puerto 8080 (o el puerto que utilice tu aplicación Spring Boot)
EXPOSE 8080

# Comando para ejecutar la aplicación al iniciar el contenedor
CMD ["java", "-jar", "app.jar"]
