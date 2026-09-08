from django.urls import path
from . import views

urlpatterns = [
    # Rutas de autenticación
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    
    # Rutas del catálogo
    path('', views.index, name='index'),
    path('producto/<int:id>/', views.detalle, name='detalle'),
]
