# Usar la imagen oficial de Python 3.10
FROM python:3.10-slim-buster

# Configurar el directorio de trabajo en /app
WORKDIR /app

# Configurar el path al configmap
ENV CONFIGMAP_PATH=config/configmap.yml

# Copiar el directorio 'code' del host a /app en el contenedor
COPY ./code /app

# Instalar poetry
RUN pip install poetry

# Construir la distribución
RUN poetry build

# Instalar la distribución sin especificar la versión
RUN pip install $(ls dist/*.whl)

# Copiar el script de inicio al contenedor
COPY entrypoint.sh /app/start.sh

# Dar permisos de ejecución al script
RUN chmod +x /app/start.sh

# Ejecutar el script al iniciar el contenedor
CMD ["/app/start.sh"]
