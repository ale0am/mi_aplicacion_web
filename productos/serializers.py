from rest_framework import serializers
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido
from django.contrib.auth.models import User

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'activo', 'fecha_creacion']

class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoria.nombre', read_only=True)
    
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'descripcion', 'precio', 'categoria', 
            'categoria_nombre', 'stock', 'imagen', 'activo', 
            'fecha_creacion', 'fecha_actualizacion'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ClienteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    # Campos para crear usuario automáticamente
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'user', 'telefono', 'direccion', 'fecha_nacimiento',
            'username', 'email', 'first_name', 'last_name', 'password'
        ]
    
    def create(self, validated_data):
        # Extraer datos del usuario
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'password': validated_data.pop('password'),
        }
        
        # Crear usuario automáticamente
        user = User.objects.create_user(**user_data)
        
        # Crear cliente asociado al usuario
        cliente = Cliente.objects.create(user=user, **validated_data)
        return cliente

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio_unitario']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = DetallePedidoSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.user.get_full_name', read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente', 'cliente_nombre', 'fecha_pedido', 
            'estado', 'total', 'detalles'
        ]