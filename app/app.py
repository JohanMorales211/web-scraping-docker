# Crea la app de flask
app = Flask(__name__)

# URL base para scrappear
URL_BASE = os.getenv('URL_BASE', 'https://www.farmatodo.com.co/categorias/salud-y-medicamentos')

# Obtiene los productos de una página, por defecto la URL base
def obtener_productos(url=URL_BASE):
    """
    Obtiene los productos de una página, por defecto la URL base
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    productos = []
    for card in soup.find_all('div', class_='card-ftd__card-unique'):
        nombre = card.find('p', class_='text-title').get_text(strip=True)
        precio = card.find('span', class_='price__text-price').get_text(strip=True)
        enlace = "https://www.farmatodo.com.co" + card.find('a', class_='content-product').get('href')
        productos.append({
            'nombre': nombre,
            'precio': precio,
            'enlace': enlace
        })
    return productos

# Obtiene la info de un producto
def obtener_info_producto(url):
    """
    Obtiene la info de un producto
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    info = {}
    for item in soup.find('div', class_='data-sheet').find_all('div', class_='item'):
        title = item.find('div', class_='title').get_text(strip=True).replace(":", "")
        description = item.find('div', class_='description').get_text(strip=True)
        info[title] = description
    return info


# Endpoint para obtener los productos
@app.route('/productos', methods=['GET'])
def productos():
    """
    Obtiene los productos de la página principal, y los almacena en un archivo JSON
    """
    # Intenta cargar datos del archivo si existe
    try:
        with open('data/productos.json', 'r') as f:
            resultados = json.load(f)
    except FileNotFoundError:
        resultados = []  # Crea una lista vacía si el archivo no existe

    # Si el archivo no existe o está vacío, extrae los datos
    if not resultados:
        productos = obtener_productos()
        for producto in productos:
            info = obtener_info_producto(producto['enlace'])
            resultados.append({
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'info': info,
                'enlace': producto['enlace']
            })

        # Guarda los datos en el archivo JSON
        with open('data/productos.json', 'w') as f:
            json.dump(resultados, f, indent=4)

    return jsonify(resultados)


if __name__ == "__main__":
    """
    Inicia la app en modo debug, y en el host y puerto 5000
    """
    app.run(debug=True, host='0.0.0.0', port=5000)
