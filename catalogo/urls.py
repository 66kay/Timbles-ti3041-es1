from django.urls import path
from . import views

"""
=====================================================
URLS.PY - Rutas de la aplicación Ferretería Timbles
=====================================================
Define todas las URLs que el navegador puede visitar.
Cada ruta conecta una dirección web con una función en views.py.
"""

urlpatterns = [
    # ---- PÁGINA PÚBLICA ----
    # Ruta raíz: Landing page (no requiere login)
    path('', views.landing, name='landing'),

    # ---- AUTENTICACIÓN ----
    # Formulario de inicio de sesión
    path('login/', views.login_view, name='login_view'),
    # Cierre de sesión (redirige a la landing)
    path('logout/', views.logout_view, name='logout_view'),

    # ---- CATÁLOGO ----
    # Lista completa de productos (requiere login)
    path('catalogo/', views.index, name='index'),
    # Detalle de un producto específico por su ID
    path('producto/<int:id>/', views.detalle, name='detalle'),

    # ---- CARRITO DE COMPRAS ----
    # Ver el contenido del carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    # Agregar un producto al carrito (recibe ID por URL)
    path('carrito/agregar/<int:id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    # Ejecutar la compra (descuenta stock del JSON)
    path('carrito/comprar/', views.comprar_carrito, name='comprar_carrito'),
    # Vaciar el carrito sin comprar
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),

    # ---- ADMINISTRACIÓN (Solo admin) ----
    # Cambiar el stock de un producto
    path('gestion/modificar_stock/<int:id>/', views.modificar_stock, name='modificar_stock'),
    # Eliminar un producto del catálogo
    path('gestion/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
]
