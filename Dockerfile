FROM maven:latest as MAVEN_BUILD
COPY ./ ./
RUN --mount=type=cache,target=/root/.m2 mvn clean package
RUN mv target/*.jar target/app.jar

# Define la ubicación del controlador de GeckoDriver
ARG GECKO_DRIVER_VERSION="v0.30.0"
ARG GECKO_DRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/${GECKO_DRIVER_VERSION}/geckodriver-${GECKO_DRIVER_VERSION}-linux64.tar.gz"

# Descarga y descomprime el controlador de GeckoDriver
RUN apk --no-cache add curl tar \
    && curl -SL ${GECKO_DRIVER_URL} | tar -xz -C /usr/local/bin/
