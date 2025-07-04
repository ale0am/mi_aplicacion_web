from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

# Vista simple para la página principal
def home(request):
    return HttpResponse("""
    <h1> Mi Tienda Online - API</h1>
    <p>Bienvenido a la API de mi tienda online</p>
    <ul>
        <li><a href="/admin/">Panel de Administración</a></li>
        <li><a href="/api/">API Endpoints</a></li>
        <li><a href="/api/categorias/">Categorías</a></li>
        <li><a href="/api/productos/">Productos</a></li>
        <li><a href="/api/clientes/">Clientes</a></li>
        <li><a href="/api/pedidos/">Pedidos</a></li>
    </ul>
    """)

urlpatterns = [
    path('', home, name='home'),  # Página principal
    path('admin/', admin.site.urls),
    path('', include('productos.urls')),
    path('api-auth/', include('rest_framework.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)