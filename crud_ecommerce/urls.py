from django.contrib import admin
from django.urls import path, include
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # URLs para autenticação
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/registro/', views.registro, name='registro'),
    path('accounts/registro-admin/', views.registro_admin, name='registro_admin'),

    # URLs para o CRUD de Produtos (Admin)
    path('produtos/admin/', views.listar_produtos_admin, name='listar_produtos_admin'),
    path('produtos/novo/', views.criar_produto, name='criar_produto'),
    path('produtos/<int:pk>/', views.detalhar_produto, name='detalhar_produto'),
    path('produtos/<int:pk>/editar/', views.editar_produto, name='editar_produto'),
    path('produtos/<int:pk>/excluir/', views.excluir_produto, name='excluir_produto'),

    # URL para a listagem de produtos para clientes
    path('produtos/', views.listar_produtos_cliente, name='listar_produtos_cliente'),

    # URLs para o CRUD de Clientes (Admin)
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.criar_cliente, name='criar_cliente'),
    path('clientes/<int:pk>/', views.detalhar_cliente, name='detalhar_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/excluir/', views.excluir_cliente, name='excluir_cliente'),

    # URLs de Pedidos e Carrinho
    path('carrinho/', views.carrinho, name='carrinho'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
    path('meus-pedidos/<int:pk>/', views.detalhar_pedido, name='detalhar_pedido'),
    path('pedidos-admin/', views.listar_todos_pedidos, name='listar_todos_pedidos'),
    path('carrinho/adicionar/<int:produto_pk>/', views.adicionar_item_carrinho, name='adicionar_item_carrinho'),
    path('carrinho/remover/<int:item_pk>/', views.remover_item_carrinho, name='remover_item_carrinho'),
    path('carrinho/atualizar/<int:item_pk>/', views.atualizar_quantidade_item, name='atualizar_quantidade_item'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
]
