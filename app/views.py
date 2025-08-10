from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .models import Produto, Cliente, Pedido, ItemPedido
from .forms import ProdutoForm, ClienteForm, RegistroForm, AdminRegistroForm
from django.http import JsonResponse
import json

# Teste para verificar se o usuário é um superusuário
def is_superuser(user):
    return user.is_superuser

# View para a página inicial
def home(request):
    produtos = Produto.objects.all()
    # Caminho corrigido para o template
    return render(request, 'loja/home.html', {'produtos': produtos})

# CRUD de Produtos (Admin)

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def listar_produtos(request):
    produtos = Produto.objects.all()
    # Caminho corrigido para o template
    return render(request, 'loja/produtos.html', {'produtos': produtos})

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def criar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm()
    # Caminho corrigido para o template
    return render(request, 'loja/criar_produto.html', {'form': form})

@login_required
def detalhar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    # Caminho corrigido para o template
    return render(request, 'loja/detalhar_produto.html', {'produto': produto})

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = ProdutoForm(instance=produto)
    # Caminho corrigido para o template
    return render(request, 'loja/editar_produto.html', {'form': form, 'produto': produto})

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def excluir_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('listar_produtos')
    # Caminho corrigido para o template
    return render(request, 'loja/confirmar_exclusao_produto.html', {'produto': produto})

# CRUD de Clientes (Admin)

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def listar_clientes(request):
    clientes = Cliente.objects.all()
    # Caminho corrigido para o template
    return render(request, 'loja/clientes.html', {'clientes': clientes})

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def criar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    # Caminho corrigido para o template
    return render(request, 'loja/criar_cliente.html', {'form': form})

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def detalhar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    # Caminho corrigido para o template
    return render(request, 'loja/detalhar_clientes.html', {'cliente': cliente})

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    # Caminho corrigido para o template
    return render(request, 'loja/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    # Caminho corrigido para o template
    return render(request, 'loja/confirmar_exclusao_cliente.html', {'cliente': cliente})

# Views para o carrinho de compras
@login_required
def carrinho(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, completo=False)
    items = ItemPedido.objects.filter(pedido=pedido)
    context = {'pedido': pedido, 'items': items}
    # Caminho corrigido para o template
    return render(request, 'loja/carrinho.html', context)

@login_required
def adicionar_item_carrinho(request, produto_pk):
    produto = get_object_or_404(Produto, pk=produto_pk)
    cliente = get_object_or_404(Cliente, user=request.user)
    pedido, _ = Pedido.objects.get_or_create(cliente=cliente, completo=False)
    item, criado = ItemPedido.objects.get_or_create(
        pedido=pedido,
        produto=produto,
        defaults={'quantidade': 1, 'preco_unitario': produto.preco}
    )
    if not criado:
        item.quantidade += 1
        item.save()

    return JsonResponse({'message': 'Item adicionado ao carrinho!'})

@login_required
def remover_item_carrinho(request, item_pk):
    item = get_object_or_404(ItemPedido, pk=item_pk)
    item.delete()
    return JsonResponse({'message': 'Item removido do carrinho!'})

@login_required
def atualizar_item_carrinho(request, item_pk, action):
    item = get_object_or_404(ItemPedido, pk=item_pk)
    
    if action == 'adicionar':
        item.quantidade += 1
    elif action == 'remover':
        item.quantidade -= 1
        if item.quantidade <= 0:
            item.delete()
    
    item.save()

    return JsonResponse({'message': 'Carrinho atualizado!'})

@login_required
def finalizar_compra(request):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, user=request.user)
        pedido = get_object_or_404(Pedido, cliente=cliente, completo=False)
        pedido.completo = True
        pedido.save()
        return JsonResponse({'message': 'Compra finalizada com sucesso!'})
    return JsonResponse({'message': 'Método não permitido.'}, status=405)


# Views para o histórico de pedidos
@login_required
def meus_pedidos(request):
    cliente = get_object_or_404(Cliente, user=request.user)
    pedidos = Pedido.objects.filter(cliente=cliente, completo=True).order_by('-data_pedido')
    context = {'pedidos': pedidos}
    # Caminho corrigido para o template
    return render(request, 'loja/meus_pedidos.html', context)

@login_required
def detalhar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.user.is_superuser or pedido.cliente.user == request.user:
        items = ItemPedido.objects.filter(pedido=pedido)
        context = {'pedido': pedido, 'items': items}
        # Caminho corrigido para o template
        return render(request, 'loja/detalhar_pedido.html', context)
    else:
        return redirect('meus_pedidos')

@login_required
@user_passes_test(is_superuser, login_url='/accounts/login/')
def listar_todos_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-data_pedido')
    context = {'pedidos': pedidos}
    # Caminho corrigido para o template
    return render(request, 'loja/listar_todos_pedidos.html', context)

# View de Registro de Usuário
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # Salva o novo usuário
            user = form.save()
            # Garante que o usuário cliente não seja um superusuário
            user.is_superuser = False
            user.is_staff = False
            user.save()
            # Cria o perfil de cliente
            cliente = Cliente.objects.create(
                user=user,
                # Usa o username do objeto User recém-criado
                nome=user.username,
                email=form.cleaned_data['email'],
                telefone=form.cleaned_data['telefone'],
                endereco=form.cleaned_data['endereco']
            )
            return redirect('login')
    else:
        form = RegistroForm()
    # Caminho corrigido para o template
    return render(request, 'templates/registro.html', {'form': form})


# Nova view para o registro de administradores, acessível sem login prévio
def registro_admin(request):
    if request.method == 'POST':
        form = AdminRegistroForm(request.POST)
        if form.is_valid():
            # Salva o novo usuário
            user = form.save()
            # Garante que o usuário administrador seja um superusuário
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return redirect('loja/listar_todos_pedidos')
    else:
        form = AdminRegistroForm()
    # Caminho corrigido para o template
    return render(request, 'loja/registro_admin.html', {'form': form})

# Nova view para logout
def logout_view(request):
    logout(request)
    return redirect('home')

