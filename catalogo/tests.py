
#=====================================================
#TESTS.PY - Pruebas Automatizadas de Ferretería Timbles
#=====================================================
#Este archivo contiene pruebas unitarias y de integración
#para verificar todo el funcionamiento del sistema:

#1. Integridad de los datos JSON (40 productos, imágenes y campos).
#2. Flujo completo del rol CLIENTE (cliente / cliente):
#   - Navegación pública (Landing)
#   - Redirección si no está logeado
#   - Login con credenciales de cliente
#   - Vista de catálogo y vista de detalle
#   - Manejo de error 404 para IDs inexistentes
#   - Carrito de compras (añadir, vaciar y comprar)
#   - Seguridad: un cliente NO puede modificar stock ni eliminar
#3. Flujo completo del rol ADMIN (admin / admin):
#   - Login con credenciales de administrador
#   - Visualización de botones y controles de administración
#   - Modificación de stock
#   - Eliminación de productos
#4. Cierre de sesión (Logout)


import os
import json
import shutil
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings


class CatalogoTestSuite(TestCase):
    
    def setUp(self):
        """
        Se ejecuta antes de CADA prueba.
        Crea un respaldo de productos.json para que las pruebas
        de compra, modificación y eliminación no alteren los datos reales.
        """
        self.client = Client()
        self.json_path = os.path.join(settings.BASE_DIR, 'catalogo', 'datos', 'productos.json')
        self.backup_path = self.json_path + '.backup_test'
        
        # Hacemos una copia de respaldo del archivo JSON original
        if os.path.exists(self.json_path):
            shutil.copyfile(self.json_path, self.backup_path)

    def tearDown(self):
        """
        Se ejecuta al terminar CADA prueba.
        Restaura el archivo productos.json original desde el respaldo.
        """
        if os.path.exists(self.backup_path):
            try:
                shutil.copyfile(self.backup_path, self.json_path)
                os.remove(self.backup_path)
            except PermissionError:
                pass

    # 1. PRUEBAS DE DATOS (REQUISITOS RÚBRICA INACAP ES1)

    def test_01_datos_json_40_productos(self):
        """Verifica que el JSON contenga exactamente 40 productos (Variante Ferretería)."""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            productos = json.load(f)
        self.assertEqual(len(productos), 40, "El catálogo debe tener exactamente 40 productos.")

    def test_02_campos_obligatorios_e_imagenes_existen(self):
        """Verifica que cada producto tenga todos los campos requeridos y que su imagen exista."""
        campos_esperados = ['id', 'nombre', 'marca', 'categoria', 'precio', 'stock', 'descripcion', 'imagen']
        with open(self.json_path, 'r', encoding='utf-8') as f:
            productos = json.load(f)

        for prod in productos:
            for campo in campos_esperados:
                self.assertIn(campo, prod, f"El producto ID {prod.get('id')} no tiene el campo '{campo}'.")
            
            # Verificamos que la imagen exista físicamente en la carpeta estática
            img_relativa = prod['imagen'].lstrip('/')
            img_fisica = os.path.join(settings.BASE_DIR, 'catalogo', img_relativa)
            self.assertTrue(os.path.exists(img_fisica), f"No se encontró la imagen: {img_fisica}")

    def test_03_destacado_condicional_productos_sin_stock(self):
        """Verifica que existan productos con stock 0 para probar el destacado condicional."""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            productos = json.load(f)
        agotados = [p for p in productos if p['stock'] == 0]
        self.assertGreater(len(agotados), 0, "Debe haber al menos un producto con stock 0 para la Etapa 3.")

    # PRUEBAS DE NAVEGACIÓN Y LOGIN

    def test_04_landing_publica(self):
        """La página de inicio (landing) debe ser accesible sin login (HTTP 200)."""
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ferretería Timbles")

    def test_05_redireccion_sin_login(self):
        """Si un usuario no autenticado intenta ver el catálogo, debe ser redirigido al login."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login_view'), response.url)

    def test_06_login_credenciales_incorrectas(self):
        """Un intento de inicio de sesión erróneo debe mostrar mensaje de error."""
        response = self.client.post(reverse('login_view'), {
            'usuario': 'usuario_falso',
            'contrasena': 'clave_falsa'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Usuario o contraseña incorrectos")

    # PRUEBAS DE ROL CLIENTE (cliente / cliente)

    def test_07_login_cliente_exitoso(self):
        """El cliente puede iniciar sesión correctamente y es redirigido al catálogo."""
        response = self.client.post(reverse('login_view'), {
            'usuario': 'cliente',
            'contrasena': 'cliente'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('index'))
        self.assertEqual(self.client.session.get('role'), 'user')
        self.assertEqual(self.client.session.get('usuario'), 'Cliente')

    def test_08_cliente_ve_catalogo_y_resumen(self):
        """El cliente autenticado ve el catálogo, el resumen calculado y NO ve controles de admin."""
        self.client.post(reverse('login_view'), {'usuario': 'cliente', 'contrasena': 'cliente'})
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        # Resumen calculado
        self.assertContains(response, "Total Productos")
        self.assertContains(response, "Disponibles con Stock")
        self.assertContains(response, "Sin Stock (Agotados)")
        # NO debe contener botones de eliminar o modificar de admin
        self.assertNotContains(response, "btn-admin-delete")
        self.assertNotContains(response, "btn-admin-stock")

    def test_09_cliente_ve_detalle_producto(self):
        """El cliente puede ver el detalle de un producto con descripción y marca."""
        self.client.post(reverse('login_view'), {'usuario': 'cliente', 'contrasena': 'cliente'})
        response = self.client.get(reverse('detalle', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Martillo Carpintero")
        self.assertContains(response, "Stanley")
        self.assertContains(response, "Descripción:")

    def test_10_detalle_producto_inexistente_404(self):
        """Un ID inexistente debe generar un error HTTP 404 (Requisito 6 de la rúbrica)."""
        self.client.post(reverse('login_view'), {'usuario': 'cliente', 'contrasena': 'cliente'})
        response = self.client.get(reverse('detalle', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_11_cliente_flujo_carrito_y_compra(self):
        """Prueba añadir al carrito, ver el carrito y completar la compra descontando stock."""
        self.client.post(reverse('login_view'), {'usuario': 'cliente', 'contrasena': 'cliente'})
        
        # Leer stock inicial del producto 1
        with open(self.json_path, 'r', encoding='utf-8') as f:
            prods_antes = json.load(f)
        stock_antes = next(p['stock'] for p in prods_antes if p['id'] == 1)

        # 1. Agregar producto 1 al carrito
        response = self.client.post(reverse('agregar_al_carrito', args=[1]))
        self.assertEqual(response.status_code, 302)

        # 2. Ver el carrito
        response = self.client.get(reverse('ver_carrito'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Martillo Carpintero")

        # 3. Completar la compra
        response = self.client.post(reverse('comprar_carrito'))
        self.assertEqual(response.status_code, 302)

        # 4. Verificar que el stock disminuyó en 1 en el archivo JSON
        with open(self.json_path, 'r', encoding='utf-8') as f:
            prods_despues = json.load(f)
        stock_despues = next(p['stock'] for p in prods_despues if p['id'] == 1)
        self.assertEqual(stock_despues, stock_antes - 1, "El stock en el JSON debe reducirse en 1 tras la compra.")

    def test_12_cliente_no_puede_modificar_stock_ni_eliminar(self):
        """Un usuario con rol cliente no puede ejecutar acciones de administrador."""
        self.client.post(reverse('login_view'), {'usuario': 'cliente', 'contrasena': 'cliente'})
        
        # Intentar modificar stock
        response = self.client.post(reverse('modificar_stock', args=[1]), {'nuevo_stock': 999})
        self.assertEqual(response.status_code, 302)
        
        # Intentar eliminar producto
        response = self.client.post(reverse('eliminar_producto', args=[1]))
        self.assertEqual(response.status_code, 302)

        # Verificar que el producto 1 NO fue modificado ni eliminado
        with open(self.json_path, 'r', encoding='utf-8') as f:
            prods = json.load(f)
        p1 = next((p for p in prods if p['id'] == 1), None)
        self.assertIsNotNone(p1, "El producto 1 no debió ser eliminado por un cliente.")
        self.assertNotEqual(p1['stock'], 999, "El stock no debió ser modificado por un cliente.")

    # PRUEBAS DE ROL ADMIN (admin / admin)

    def test_13_login_admin_exitoso(self):
        """El administrador inicia sesión y tiene asignado el rol 'admin'."""
        response = self.client.post(reverse('login_view'), {
            'usuario': 'admin',
            'contrasena': 'admin'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session.get('role'), 'admin')
        self.assertEqual(self.client.session.get('usuario'), 'Administrador')

    def test_14_admin_ve_controles_gestion(self):
        """El administrador ve los botones de modificar stock y eliminar en el catálogo."""
        self.client.post(reverse('login_view'), {'usuario': 'admin', 'contrasena': 'admin'})
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ADMIN")
        self.assertContains(response, "admin-controls")
        self.assertContains(response, "btn-admin-delete")
        self.assertContains(response, "btn-admin-stock")

    def test_15_admin_modifica_stock(self):
        """El administrador cambia exitosamente el stock de un producto."""
        self.client.post(reverse('login_view'), {'usuario': 'admin', 'contrasena': 'admin'})
        
        # Cambiar el stock del producto 2 a 88 unidades
        response = self.client.post(reverse('modificar_stock', args=[2]), {'nuevo_stock': 88})
        self.assertEqual(response.status_code, 302)

        # Comprobar en el JSON
        with open(self.json_path, 'r', encoding='utf-8') as f:
            prods = json.load(f)
        p2 = next(p for p in prods if p['id'] == 2)
        self.assertEqual(p2['stock'], 88, "El administrador debe poder cambiar el stock en el JSON.")

    def test_16_admin_elimina_producto(self):
        """El administrador elimina un producto del catálogo de forma permanente."""
        self.client.post(reverse('login_view'), {'usuario': 'admin', 'contrasena': 'admin'})
        
        # Eliminar el producto 3
        response = self.client.post(reverse('eliminar_producto', args=[3]))
        self.assertEqual(response.status_code, 302)

        # Comprobar que ya no existe en el JSON
        with open(self.json_path, 'r', encoding='utf-8') as f:
            prods = json.load(f)
        self.assertIsNone(next((p for p in prods if p['id'] == 3), None), "El producto 3 debió ser eliminado.")
        self.assertEqual(len(prods), 39, "Deberían quedar 39 productos.")

    # PRUEBA DE LOGOUT

    def test_17_logout_cierra_sesion(self):
        """Al cerrar sesión, la sesión se destruye y redirige a la landing page."""
        self.client.post(reverse('login_view'), {'usuario': 'admin', 'contrasena': 'admin'})
        response = self.client.get(reverse('logout_view'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('landing'))
        self.assertFalse(self.client.session.get('logeado', False))

