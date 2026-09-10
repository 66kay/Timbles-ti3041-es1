
# VIEWS.PY - Ferretería Timbles
#Este archivo contiene la lógica del servidor (Backend):
#Lee y escribe datos en 'productos.json'.
#Gestiona la autenticación por sesiones (admin / cliente).
#Procesa el catálogo, detalle, carrito y compras.
#Permite modificar stock y eliminar productos (solo admin).


from django.shortcuts import render, redirect, Http404
import json
import os
from django.conf import settings

# Ruta directa al archivo JSON con los datos de los productos
RUTA_JSON = os.path.join(settings.BASE_DIR, 'catalogo', 'datos', 'productos.json')


# FUNCIONES AUXILIARES: LECTURA Y ESCRITURA DEL JSON

def leer_datos():
    #Lee y retorna la lista de productos desde el archivo JSON.
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        return json.load(f)


def escribir_datos(productos):
    #Sobrescribe el archivo JSON con la lista actualizada de productos.
    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)


# PÁGINA PÚBLICA (LANDING)

def landing(request):
    #Página de bienvenida pública (no requiere estar autenticado).
    return render(request, 'catalogo/landing.html')


# AUTENTICACIÓN (LOGIN Y LOGOUT)

def login_view(request):
    #Controla el inicio de sesión. Acepta dos credenciales:
    #admin / admin     -> Rol 'admin' (puede editar stock y eliminar)
    #cliente / cliente -> Rol 'user' (solo comprar y ver catálogo)
    error = None
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')

        if usuario == 'admin' and contrasena == 'admin':
            request.session['logeado'] = True
            request.session['role'] = 'admin'
            request.session['usuario'] = 'Administrador'
            return redirect('index')
        elif usuario == 'cliente' and contrasena == 'cliente':
            request.session['logeado'] = True
            request.session['role'] = 'user'
            request.session['usuario'] = 'Cliente'
            return redirect('index')
        else:
            error = "Usuario o contraseña incorrectos"

    return render(request, 'catalogo/login.html', {'error': error})


def logout_view(request):
    #Cierra la sesión eliminando los datos guardados y redirige a la landing.
    request.session.flush()
    return redirect('landing')


# CATÁLOGO Y DETALLE DE PRODUCTOS

def index(request):
    #Muestra el catálogo con todos los productos y el resumen estadístico:
    #total productos, disponibles, sin stock y unidades totales en bodega.
    
    if not request.session.get('logeado'):
        return redirect('login_view')

    productos = leer_datos()
    carrito = request.session.setdefault('carrito', [])

    # Cálculos matemáticos solicitados en la rúbrica (Etapa 3)
    total_productos = len(productos)
    disponibles = sum(1 for p in productos if p['stock'] > 0)
    sin_stock = sum(1 for p in productos if p['stock'] == 0)
    total_stock = sum(p['stock'] for p in productos)

    contexto = {
        'productos': productos,
        'total_productos': total_productos,
        'disponibles': disponibles,
        'sin_stock': sin_stock,
        'total_stock': total_stock,
        'carrito_count': len(carrito),
        'role': request.session.get('role', 'user'),
        'usuario': request.session.get('usuario', '')
    }
    return render(request, 'catalogo/lista.html', contexto)


def detalle(request, id):
    #Muestra la ficha técnica de un producto individual por su ID.
    #Si el ID no existe en el JSON, responde con un error 404.
    
    if not request.session.get('logeado'):
        return redirect('login_view')

    productos = leer_datos()
    producto = next((p for p in productos if p['id'] == id), None)

    if not producto:
        raise Http404("Producto no encontrado en la base de datos")

    total_stock = sum(p['stock'] for p in productos)
    carrito = request.session.get('carrito', [])

    contexto = {
        'producto': producto,
        'total_stock': total_stock,
        'carrito_count': len(carrito),
        'role': request.session.get('role', 'user'),
        'usuario': request.session.get('usuario', '')
    }
    return render(request, 'catalogo/detalle.html', contexto)



# 4. CARRITO DE COMPRAS

def agregar_al_carrito(request, id):
    #Agrega el ID de un producto a la lista del carrito en la sesión.
    if not request.session.get('logeado'):
        return redirect('login_view')

    if request.method == 'POST':
        carrito = request.session.get('carrito', [])
        carrito.append(id)
        request.session['carrito'] = carrito

    return redirect('index')


def ver_carrito(request):
    #Muestra los productos agregados al carrito y calcula el total a pagar.
    if not request.session.get('logeado'):
        return redirect('login_view')

    carrito_ids = request.session.get('carrito', [])
    productos = leer_datos()

    # Buscamos cada producto del carrito para obtener nombre, imagen y precio
    productos_carrito = []
    total_precio = 0
    for pid in carrito_ids:
        for p in productos:
            if p['id'] == pid:
                productos_carrito.append(p)
                total_precio += p['precio']
                break

    contexto = {
        'productos_carrito': productos_carrito,
        'total_precio': total_precio,
        'carrito_count': len(carrito_ids),
        'role': request.session.get('role', 'user'),
        'usuario': request.session.get('usuario', '')
    }
    return render(request, 'catalogo/carrito.html', contexto)


def vaciar_carrito(request):
    #Vacía los productos del carrito en la sesión sin realizar compra.
    if not request.session.get('logeado'):
         return redirect('login_view')

    if request.method == 'POST':
        request.session['carrito'] = []

    return redirect('ver_carrito')


def comprar_carrito(request):
    #Confirma la compra: descuenta 1 unidad de stock en el JSON por cada
    #producto en el carrito (si hay stock > 0) y luego vacía el carrito.
    
    if not request.session.get('logeado'):
        return redirect('login_view')

    if request.method == 'POST':
        carrito_ids = request.session.get('carrito', [])
        productos = leer_datos()

        # Descontamos 1 unidad de stock por cada ítem en el carrito
        for pid in carrito_ids:
            for p in productos:
                if p['id'] == pid and p['stock'] > 0:
                    p['stock'] -= 1
                    break

        escribir_datos(productos)
        request.session['carrito'] = []

    return redirect('index')


# GESTIÓN DE ADMINISTRADOR (SOLO ADMIN)

def modificar_stock(request, id):
    #Permite al administrador modificar manualmente el stock de un producto.
    
    if not request.session.get('logeado'):
        return redirect('login_view')
    if request.session.get('role') != 'admin':
        return redirect('index')

    if request.method == 'POST':
        try:
            nuevo_stock = max(0, int(request.POST.get('nuevo_stock', 0)))
        except (ValueError, TypeError):
            return redirect('index')

        productos = leer_datos()
        for p in productos:
            if p['id'] == id:
                p['stock'] = nuevo_stock
                break
        escribir_datos(productos)

    # Si vino desde la ficha de detalle, permanece en la ficha
    referer = request.META.get('HTTP_REFERER', '')
    if f'/producto/{id}/' in referer:
        return redirect('detalle', id=id)

    return redirect('index')


def eliminar_producto(request, id):
    #Permite al administrador eliminar un producto del catálogo permanentemente.
    
    if not request.session.get('logeado'):
        return redirect('login_view')
    if request.session.get('role') != 'admin':
        return redirect('index')

    if request.method == 'POST':
        productos = leer_datos()
        # Filtramos la lista conservando solo los productos con ID diferente
        productos = [p for p in productos if p['id'] != id]
        escribir_datos(productos)

    return redirect('index')
