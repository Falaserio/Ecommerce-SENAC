from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Produto, Cliente, Pedido, ItemPedido
from .forms import ProdutoForm, ClienteForm

# Teste para verificar se o usuário é um superusuário
def is_superuser(user):
    return user.is_superuser

# View para a página inicial
def home(request):
    return render(request, 'F:/crud_ecommerce/app/templates/loja/home.html')

# CRUD de Produtos

@login_required
@user_passes_test(is_superuser)
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'F:/crud_ecommerce/app/templates/produtos.html', {'produtos': produtos})

@login_required
@user_passes_test(is_superuser)
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'F:/crud_ecommerce/app/templates/criar_produtos.html', {'form': form})

@login_required
def detalhar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'F:/crud_ecommerce/app/templates/detalhar_produto.html', {'produto': produto})

@login_required
@user_passes_test(is_superuser)
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'F:/crud_ecommerce/app/templates/editar_produto.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    return render(request, 'F:/crud_ecommerce/app/templates/excluir_produto.html', {'produto': produto})


# CRUD de Clientes

@login_required
@user_passes_test(is_superuser)
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'F:/crud_ecommerce/app/templates/clientes.html', {'clientes': clientes})

@login_required
@user_passes_test(is_superuser)
def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'F:/crud_ecommerce/app/templates/criar_cliente.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def detalhar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'F:/crud_ecommerce/app/templates/detalhar_cliente.html', {'cliente': cliente})

@login_required
@user_passes_test(is_superuser)
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'F:/crud_ecommerce/app/templates/editar_cliente.html', {'form': form})

@login_required
@user_passes_test(is_superuser)
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'F:/crud_ecommerce/app/templates/excluir_cliente.html', {'cliente': cliente})
