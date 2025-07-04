# productos/admin.py
from django.contrib import admin
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo']
    list_filter = ['categoria', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['user', 'telefono']
    search_fields = ['user__username', 'user__email']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_pedido', 'estado', 'total']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['cliente__user__username']

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario']