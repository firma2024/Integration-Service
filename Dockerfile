# Utiliza una imagen de Java como base para compilar
FROM maven:latest AS build

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de tu proyecto al contenedor
COPY . /app

# Compila tu aplicación Java usando Maven
RUN mvn clean install

# Utiliza una imagen de Java como base para la ejecución
FROM openjdk:17-jdk-alpine
FROM selenium/standalone-firefox:latest
WORKDIR /app

# Copia los archivos generados (incluyendo el .jar) desde la imagen anterior al contenedor final
COPY --from=build /app/target/integracion-0.0.1-SNAPSHOT.jar /app
# Define el comando a ejecutar cuando se inicie el contenedor
CMD ["java", "-jar", "integracion-0.0.1-SNAPSHOT.jar"]

EXPOSE 8080