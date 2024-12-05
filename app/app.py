# Modulo principal del scraper, contiene funciones para obtener los productos de una
# página y obtener la información de un producto en particular.
import os
import csv
import requests
from bs4 import BeautifulSoup
import logging

# URL base para scrappear
URL_BASE = os.getenv('URL_BASE', 'https://www.farmatodo.com.co/categorias/salud-y-medicamentos')

# Recibe la URL de la página y devuelve una lista de diccionarios con la info de cada producto.
# El diccionario contiene las claves nombre, precio y enlace
def obtener_productos(url=URL_BASE):
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

# Recibe la URL de la página del producto y devuelve un diccionario con la info del producto
def obtener_info_producto(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    info = {}
    for item in soup.find('div', class_='data-sheet').find_all('div', class_='item'):
        title = item.find('div', class_='title').get_text(strip=True).replace(":", "")
        description = item.find('div', class_='description').get_text(strip=True)
        info[title] = description
    return info

def main():
    # Crear el directorio data si no existe
    if not os.path.exists('data'):
        os.makedirs('data')

    # Obtener los productos
    productos = obtener_productos()

    # Preparar los datos para el CSV
    all_data = []
    for producto in productos:
        info = obtener_info_producto(producto['enlace'])
        # Combinar el producto y su información
        combined = {**producto, **info}
        all_data.append(combined)

    # Recopilar todas las claves únicas de todos los diccionarios
    all_keys = set()
    for data in all_data:
        all_keys.update(data.keys())
    fieldnames = list(all_keys)

    # Escribir en el archivo CSV
    if all_data:
        with open('data/productos.csv', 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(all_data)

if __name__ == "__main__":
    main()
