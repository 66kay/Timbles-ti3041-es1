from django.shortcuts import render, Http404
import json
import os
from django.conf import settings

# Función para leer el archivo JSON que simula nuestra base de datos.
# Se usa os.path.join para construir la ruta correcta hacia catalogo/datos/productos.json
def leer_datos():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'datos', 'productos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

# Vista principal que muestra todos los productos
def index(request):
    productos = leer_datos() # Leemos todos los productos
    # Renderizamos la página 'lista.html' y le enviamos la variable 'productos'
    return render(request, 'catalogo/lista.html', {'productos': productos})

# Vista para mostrar un solo producto según su ID
def detalle(request, id):
    productos = leer_datos()
    # Buscamos el producto en la lista cuyo ID coincida con el que viene en la URL
    producto = next((p for p in productos if p['id'] == id), None)
    
    # Manejo de error 404: Si no encontramos el producto, mostramos un error
    if producto is None:
        raise Http404("Producto no encontrado en la base de datos")
        
    # Si existe, renderizamos la página 'detalle.html' pasándole el producto encontrado
    return render(request, 'catalogo/detalle.html', {'producto': producto})
