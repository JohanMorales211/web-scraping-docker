# Web Scraping con Docker y SQL Server

Este proyecto realiza web scraping de productos de Farmatodo (configurables mediante la variable de entorno `URL_BASE`), extrae información detallada de cada producto y almacena los datos en una base de datos SQL Server ejecutándose en Docker.

![Farmatodo](https://gestionsolidaria.com/wp-content/uploads/2019/03/FACHADA-FARMATODO-NUEVA_OK-RESOLUCION.jpg)
![Docker](https://datascientest.com/en/files/2023/10/docker-tutorial.webp)

## Estructura del Proyecto

```
web-scraping-docker/
├─ .gitignore
├─ app/
│   ├─ app.py         # Script principal de scraping
│   └─ __init__.py
├─ db/
│   └─ Dockerfile     # Dockerfile para la base de datos SQL Server
├─ docker-compose.yml  # Orquesta la aplicación y la base de datos
├─ Dockerfile         # Dockerfile para la aplicación de scraping
└─ requirements.txt    # Dependencias de Python
```

## Cómo Ejecutar el Proyecto

1. **Clonar el repositorio:**

```bash
git clone https://github.com/JohanMorales211/web-scraping-docker.git
cd web-scraping-docker
```

2. **Construir y ejecutar los contenedores:**

```bash
docker-compose up -d --build
```

Este comando construirá las imágenes Docker para la aplicación de scraping y la base de datos SQL Server, y luego las ejecutará en segundo plano.  Los datos scrapeados se guardarán en un archivo CSV en la carpeta `db/data` dentro del contenedor,  y se importarán a la base de datos SQL Server.

3. **Verificar los logs:**  Puedes monitorizar el progreso del scraping y la creación de la base de datos con:

```bash
docker-compose logs -f
```

## Comandos Útiles

### Reiniciar desde cero (borrando volúmenes y contenedores):

Este comando detendrá los contenedores, eliminará los volúmenes (incluyendo la base de datos) y las imágenes construidas, y luego volverá a construir y ejecutar todo:

```bash
docker-compose down -v --rmi all --remove-orphans
docker-compose up -d --build
```

### Detener los contenedores:

```bash
docker-compose down
```

### Reconstruir las imágenes:

Si se modifica el código fuente, es necesario reconstruir las imágenes:

```bash
docker-compose up -d --build
```

### Acceder a la base de datos SQL Server:

Puedes usar `sqlcmd` para conectarte a la base de datos SQL Server dentro del contenedor:

```bash
docker ps
```

```bash
docker exec -it <contenedor_db> /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P YourStrongPassw0rd -d master
```

Reemplaza `<contenedor_db>` con el nombre del contenedor de la base de datos (que se puede obtener con `docker ps`). Una vez dentro, puedes ejecutar consultas SQL para verificar los datos scrapeados.  Por ejemplo:

```sql
USE master;
SELECT * FROM Productos;
```

## Variables de Entorno

Puedes configurar la URL base para el scraping modificando la variable de entorno `URL_BASE` en el archivo `docker-compose.yml`. Por defecto, está configurada para `https://www.farmatodo.com.co/categorias/salud-y-medicamentos`.  **Importante:** Si cambias la URL base, ten en cuenta que el código de scraping (específicamente las selecciones de CSS en `app.py`) está diseñado para la estructura HTML de Farmatodo.  Si el sitio web objetivo tiene una estructura diferente, deberás modificar el código de scraping para que funcione correctamente.


## Dependencias

Las dependencias de Python se listan en el archivo `requirements.txt` e incluyen:

* `requests` (Para realizar peticiones HTTP)
* `beautifulsoup4` (Para parsear HTML)
* `selenium` (Para web scraping dinámico, aunque no se usa actualmente en el código)


## Creado por

Johan Morales - [Portafolio Personal](https://73tmxc.csb.app/)
