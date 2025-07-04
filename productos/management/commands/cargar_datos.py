# Crear archivo productos/management/commands/cargar_datos.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from productos.models import Categoria, Producto, Cliente

class Command(BaseCommand):
    help = 'Cargar datos de ejemplo'

    def handle(self, *args, **options):
        # Crear categorías
        categorias = [
            {'nombre': 'Electrónicos', 'descripcion': 'Dispositivos electrónicos'},
            {'nombre': 'Ropa', 'descripcion': 'Vestimenta y accesorios'},
            {'nombre': 'Hogar', 'descripcion': 'Artículos para el hogar'},
        ]
        
        for cat_data in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={'descripcion': cat_data['descripcion']}
            )
            if created:
                self.stdout.write(f'Categoría creada: {categoria.nombre}')

        # Crear productos
        electronica = Categoria.objects.get(nombre='Electrónicos')
        ropa = Categoria.objects.get(nombre='Ropa')
        
        productos = [
            {
                'nombre': 'Smartphone Samsung',
                'descripcion': 'Teléfono inteligente de última generación',
                'precio': 599.99,
                'categoria': electronica,
                'stock': 50
            },
            {
                'nombre': 'Camiseta Polo',
                'descripcion': 'Camiseta polo de algodón',
                'precio': 29.99,
                'categoria': ropa,
                'stock': 100
            },
        ]
        
        for prod_data in productos:
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Producto creado: {producto.nombre}')

        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente'))