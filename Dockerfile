# Usamos la imagen de python en su versión
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instalar las dependencias necesarias para bcp y sqlcmd
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    procps \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg \
    && curl -fsSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools unixodbc-dev \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc \
    && bash -c 'source ~/.bashrc'

# Agregar correctamente sqlcmd a PATH usando ENV
ENV PATH="/opt/mssql-tools/bin:${PATH}"

# Copia el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Instalamos las dependencias que se encuentran en requirements.txt
RUN pip install -r requirements.txt

# Copia el resto del código fuente en el directorio de trabajo
COPY . /app

# Exponer el puerto 5000 para que pueda ser accedido desde fuera del contenedor
EXPOSE 5000

# Establece la orden para ejecutar el programa principal
CMD ["python", "app/app.py"]