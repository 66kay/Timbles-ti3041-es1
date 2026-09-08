"""
=====================================================
VIEWS.PY - Controlador principal de Ferretería Timbles
=====================================================
Este archivo contiene todas las funciones (vistas) que procesan
las solicitudes del navegador y devuelven las páginas HTML.

Funciones principales:
  - landing()           → Página de bienvenida pública
  - login_view()        → Inicio de sesión (admin o cliente)
  - logout_view()       → Cierre de sesión
  - index()             → Catálogo de productos
  - detalle()           → Vista individual de un producto
  - agregar_al_carrito() → Agrega un producto al carrito
  - ver_carrito()       → Muestra el contenido del carrito
  - comprar_carrito()   → Ejecuta la compra y descuenta stock
  - vaciar_carrito()    → Vacía el carrito sin comprar
  - modificar_stock()   → [ADMIN] Cambia el stock de un producto
  - eliminar_producto() → [ADMIN] Elimina un producto del catálogo
"""

from django.shortcuts import render, redirect, Http404
import json
import os
from django.conf import settings


# =====================================================
# FUNCIONES DE LECTURA/ESCRITURA DEL ARCHIVO JSON
# =====================================================

def leer_datos():
    """
    Lee el archivo productos.json y retorna una lista de diccionarios.
    Cada diccionario representa un producto con: id, nombre, categoria,
    precio, stock e imagen.
    """
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'datos', 'productos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def escribir_datos(productos):
    """
    Recibe una lista de productos (diccionarios) y la guarda
    de vuelta en el archivo JSON, sobreescribiendo el contenido anterior.
    Se usa después de comprar o modificar el stock.
    """
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'datos', 'productos.json')
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)


# =====================================================
# VISTAS DE AUTENTICACIÓN (LOGIN / LOGOUT)
# =====================================================

def login_view(request):
    """
    Maneja el inicio de sesión. Acepta dos tipos de usuario:
      - admin / admin    → Rol 'admin' (puede modificar stock y eliminar)
      - cliente / cliente → Rol 'user' (solo puede comprar)
    
    Si las credenciales son incorrectas, muestra un mensaje de error.
    Los datos del usuario se guardan en la sesión de Django.
    """
    error = None

    # Solo procesamos cuando el usuario envía el formulario (POST)
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        # Verificamos las credenciales del administrador
        if usuario == 'admin' and contrasena == 'admin':
            request.session['logeado'] = True
            request.session['role'] = 'admin'
            request.session['usuario'] = 'Administrador'
            return redirect('index')

        # Verificamos las credenciales del cliente
        elif usuario == 'cliente' and contrasena == 'cliente':
            request.session['logeado'] = True
            request.session['role'] = 'user'
            request.session['usuario'] = 'Cliente'
            return redirect('index')

        # Si no coincide ninguna, mostramos error
        else:
            error = "Usuario o contraseña incorrectos"

    return render(request, 'catalogo/login.html', {'error': error})


def logout_view(request):
    """
    Cierra la sesión del usuario eliminando todos los datos
    almacenados en la sesión (carrito, rol, etc.) y lo redirige
    a la página de inicio (landing).
    """
    request.session.flush()
    return redirect('landing')


# =====================================================
# LANDING PAGE (Página de bienvenida pública)
# =====================================================

def landing(request):
    """
    Muestra la página de bienvenida de la ferretería.
    Esta página es pública (no requiere inicio de sesión).
    Contiene un hero section y las categorías de productos.
    """
    return render(request, 'catalogo/landing.html')


# =====================================================
# VISTAS DEL CATÁLOGO DE PRODUCTOS
# =====================================================

def index(request):
    """
    Vista principal del catálogo. Muestra todos los productos
    en formato de tarjetas (cards) con sus imágenes, precios y stock.
    
    Si el usuario es admin, también muestra los controles para
    modificar stock y eliminar productos.
    
    Los productos con stock = 0 se muestran con la etiqueta "SIN STOCK".
    """
    # Si no está logeado, lo mandamos al login
    if not request.session.get('logeado'):
        return redirect('login_view')

    # Inicializamos el carrito en la sesión si no existe
    if 'carrito' not in request.session:
        request.session['carrito'] = []

    # Leemos todos los productos del JSON
    productos = leer_datos()

    # Cálculos estadísticos para el resumen (requisito Etapa 3)
    total_productos = len(productos)
    disponibles = sum(1 for p in productos if p['stock'] > 0)
    sin_stock = sum(1 for p in productos if p['stock'] == 0)
    total_stock = sum(producto['stock'] for producto in productos)

    # Enviamos los datos calculados al template lista.html
    return render(request, 'catalogo/lista.html', {
        'productos': productos,
        'total_productos': total_productos,
        'disponibles': disponibles,
        'sin_stock': sin_stock,
        'total_stock': total_stock,
        'carrito_count': len(request.session['carrito']),
        'role': request.session.get('role', 'user'),
        'usuario': request.session.get('usuario', '')
    })


def detalle(request, id):
    """
    Muestra la información completa de un producto específico.
    Recibe el ID del producto por la URL (ej: /producto/5/).
    Si el producto no existe, lanza un error 404.
    """
    if not request.session.get('logeado'):
        return redirect('login_view')

    productos = leer_datos()
    total_stock = sum(producto['stock'] for producto in productos)

    # Buscamos el producto con el ID recibido
    producto = next((p for p in productos if p['id'] == id), None)

    # Si no lo encontramos, mostramos error 404
    if producto is None:
        raise Http404("Producto no encontrado en la base de datos")

    carrito_count = len(request.session.get('carrito', []))

    return render(request, 'catalogo/detalle.html', {
        'producto': producto,
        'total_stock': total_stock,
        'carrito_count': carrito_count,
        'role': request.session.get('role', 'user'),
        'usuario': request.session.get('usuario', '')
    })


# =====================================================
# VISTAS DEL CARRITO DE COMPRAS
# =====================================================

def agregar_al_carrito(request, id):
    """
    Agrega un producto al carrito de compras del usuario.
    El carrito se almacena como una lista de IDs en la sesión.
    Solo funciona con método POST (por seguridad).
    """
    if not request.session.get('logeado'):
        return redirect('login_view')

    if request.method == 'POST':
        carrito = request.session.get('carrito', [])
        carrito.append(id)  # Agregamos el ID del producto
        request.session['carrito'] = carrito

    return redirect('index')


def ver_carrito(request):
    """
    Muestra el contenido actual del carrito con el detalle
    de cada producto y el total a pagar.
    """
    if not request.session.get('logeado'):
        return redirect('login_view')

    carrito_ids = request.session.get('carrito', [])
    productos = leer_datos()

    # Armamos la lista de productos del carrito con sus datos completos
    productos_en_carrito = []
    total_precio = 0

    for p_id in carrito_ids:
        producto = next((p for p in productos if p['id'] == p_id), None)
        if producto:
            productos_en_carrito.append(producto)
            total_precio += producto['precio']

    return render(request, 'catalogo/carrito.html', {
        'productos_carrito': productos_en_carrito,
        'total_precio': total_precio,
        'carrito_count': len(carrito_ids),
        'role': request.session.get('role', 'user'),
        'usuario': request.session.get('usuario', '')
    })


def vaciar_carrito(request):
    """
    Vacía el carrito sin realizar la compra.
    Solo funciona con método POST.
    """
    if not request.session.get('logeado'):
        return redirect('login_view')

    if request.method == 'POST':
        request.session['carrito'] = []
    return redirect('ver_carrito')


def comprar_carrito(request):
    """
    Ejecuta la compra: recorre cada producto del carrito y le resta 1
    al stock en el archivo JSON. Luego vacía el carrito.
    Solo descuenta si el producto tiene stock mayor a 0.
    """
    if not request.session.get('logeado'):
        return redirect('login_view')

    if request.method == 'POST':
        carrito_ids = request.session.get('carrito', [])
        productos = leer_datos()

        # Recorremos cada producto del carrito
        for p_id in carrito_ids:
            for p in productos:
                if p['id'] == p_id and p['stock'] > 0:
                    p['stock'] -= 1  # Descontamos 1 unidad
                    break

        # Guardamos los cambios en el archivo JSON
        escribir_datos(productos)
        # Vaciamos el carrito de la sesión
        request.session['carrito'] = []

    return redirect('index')


# =====================================================
# VISTAS DE ADMINISTRACIÓN (Solo para rol 'admin')
# =====================================================

def modificar_stock(request, id):
    """
    [SOLO ADMIN] Permite cambiar el stock de un producto.
    Recibe el nuevo valor desde un formulario numérico.
    Si el valor es negativo, se ajusta a 0.
    """
    if not request.session.get('logeado'):
        return redirect('login_view')

    # Verificamos que el usuario sea administrador
    if request.session.get('role') != 'admin':
        return redirect('index')

    if request.method == 'POST':
        nuevo_stock = request.POST.get('nuevo_stock')
        try:
            nuevo_stock = int(nuevo_stock)
            if nuevo_stock < 0:
                nuevo_stock = 0
        except (ValueError, TypeError):
            return redirect('index')

        # Buscamos el producto y actualizamos su stock
        productos = leer_datos()
        for p in productos:
            if p['id'] == id:
                p['stock'] = nuevo_stock
                break
        escribir_datos(productos)

    # Si vino desde la página de detalle, nos quedamos en el detalle
    referer = request.META.get('HTTP_REFERER', '')
    if f'/producto/{id}/' in referer:
        return redirect('detalle', id=id)

    return redirect('index')


def eliminar_producto(request, id):
    """
    [SOLO ADMIN] Elimina un producto del catálogo de forma permanente.
    Filtra la lista de productos excluyendo el ID recibido
    y guarda el resultado en el JSON.
    """
    if not request.session.get('logeado'):
        return redirect('login_view')

    # Verificamos que el usuario sea administrador
    if request.session.get('role') != 'admin':
        return redirect('index')

    if request.method == 'POST':
        productos = leer_datos()
        # Creamos una nueva lista sin el producto eliminado
        productos = [p for p in productos if p['id'] != id]
        escribir_datos(productos)

    return redirect('index')
