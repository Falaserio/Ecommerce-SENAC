from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # URLs para o CRUD de Produtos
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('produtos/novo/', views.criar_produto, name='criar_produto'),
    path('produtos/<int:pk>/', views.detalhar_produto, name='detalhar_produto'),
    path('produtos/<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/<int:pk>/excluir/', views.excluir_produto, name='excluir_produto'),

    # URLs para o CRUD de Clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
    path('clientes/<int:pk>/', views.detalhar_cliente, name='detalhar_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/excluir/', views.excluir_cliente, name='excluir_cliente'),

    # URLs de autenticação do Django
    path('accounts/', include('django.contrib.auth.urls')),
]
