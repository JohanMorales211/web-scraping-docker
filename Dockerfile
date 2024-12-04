# Usamos la imagen de python en su version
FROM python:3.9-slim

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Copiamos el archivo requirements.txt en el directorio de trabajo
COPY requirements.txt .

# Instalamos las dependencias que se encuentran en requirements.txt
RUN pip install -r requirements.txt

# Copiamos el resto del c digo fuente en el directorio de trabajo
COPY . /app

# Exponemos el puerto 5000 para que pueda ser accedido desde fuera del contenedor
EXPOSE 5000

# Establecemos la orden para ejecutar el programa principal
CMD ["python", "app/app.py"]
