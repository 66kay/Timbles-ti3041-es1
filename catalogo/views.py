from django.shortcuts import render, Http404
import json
import os
from django.conf import settings

# Función para leer el archivo JSON que simula nuestra base de datos.
def leer_datos():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'datos', 'productos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

# Vista principal que muestra todos los productos
def index(request):
    productos = leer_datos()
    
    # NUEVO ETAPA 3: Calculamos la suma total de todo el stock de todos los productos
    total_stock = sum(producto['stock'] for producto in productos)
    
    # Enviamos tanto la lista de 'productos' como el 'total_stock' al HTML
    return render(request, 'catalogo/lista.html', {
        'productos': productos, 
        'total_stock': total_stock
    })

# Vista para mostrar un solo producto según su ID
def detalle(request, id):
    productos = leer_datos()
    # NUEVO ETAPA 3: También calculamos el stock total aquí para que la cabecera (base.html) no se rompa al ver el detalle
    total_stock = sum(producto['stock'] for producto in productos)
    
    producto = next((p for p in productos if p['id'] == id), None)
    
    if producto is None:
        raise Http404("Producto no encontrado en la base de datos")
        
    return render(request, 'catalogo/detalle.html', {
        'producto': producto,
        'total_stock': total_stock
    })
