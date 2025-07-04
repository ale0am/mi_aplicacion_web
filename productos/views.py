from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Categoria, Producto, Cliente, Pedido, DetallePedido
from .serializers import (
    CategoriaSerializer, ProductoSerializer, 
    ClienteSerializer, PedidoSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    @action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        """Obtener productos de una categoría específica"""
        categoria = self.get_object()
        productos = Producto.objects.filter(categoria=categoria, activo=True)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria_id = self.request.query_params.get('categoria', None)
        if categoria_id is not None:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Obtener productos disponibles (con stock > 0)"""
        productos = Producto.objects.filter(activo=True, stock__gt=0)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    @action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        """Cambiar estado de un pedido"""
        pedido = self.get_object()
        nuevo_estado = request.data.get('estado')
        
        if nuevo_estado in dict(Pedido.ESTADO_CHOICES):
            pedido.estado = nuevo_estado
            pedido.save()
            serializer = self.get_serializer(pedido)
            return Response(serializer.data)
        
        return Response(
            {'error': 'Estado inválido'}, 
            status=status.HTTP_400_BAD_REQUEST
        )