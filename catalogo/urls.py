from django.urls import path
from . import views

urlpatterns = [
    # Ruta vacía: Al entrar al inicio, llama a views.index
    path('', views.index, name='index'),
    # Ruta con parámetro <int:id>: Pasa un número (ID) a views.detalle
    path('producto/<int:id>/', views.detalle, name='detalle'),
]
