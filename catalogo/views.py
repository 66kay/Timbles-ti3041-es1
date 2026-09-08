from django.shortcuts import render, redirect, Http404
import json
import os
from django.conf import settings

# Función para leer el archivo JSON que simula nuestra base de datos.
def leer_datos():
    ruta = os.path.join(settings.BASE_DIR, 'catalogo', 'datos', 'productos.json')
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

# VISTA DE LOGIN: Maneja el inicio de sesión
def login_view(request):
    error = None
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        contrasena = request.POST.get('contrasena')
        
        # Validamos que sea exactamente admin / admin
        if usuario == 'admin' and contrasena == 'admin':
            # Guardamos en la sesión que el usuario está logueado
            request.session['logeado'] = True
            return redirect('index')
        else:
            error = "Usuario o contraseña incorrectos"
            
    return render(request, 'catalogo/login.html', {'error': error})

# VISTA DE LOGOUT: Cierra la sesión
def logout_view(request):
    # Borramos los datos de sesión
    request.session.flush()
    return redirect('login_view')

# Vista principal que muestra todos los productos
def index(request):
    # PROTECCIÓN: Si no está logeado, lo mandamos al login
    if not request.session.get('logeado'):
        return redirect('login_view')
        
    productos = leer_datos()
    total_stock = sum(producto['stock'] for producto in productos)
    
    return render(request, 'catalogo/lista.html', {
        'productos': productos, 
        'total_stock': total_stock
    })

# Vista para mostrar un solo producto según su ID
def detalle(request, id):
    # PROTECCIÓN: Si no está logeado, lo mandamos al login
    if not request.session.get('logeado'):
        return redirect('login_view')
        
    productos = leer_datos()
    total_stock = sum(producto['stock'] for producto in productos)
    
    producto = next((p for p in productos if p['id'] == id), None)
    
    if producto is None:
        raise Http404("Producto no encontrado en la base de datos")
        
    return render(request, 'catalogo/detalle.html', {
        'producto': producto,
        'total_stock': total_stock
    })
