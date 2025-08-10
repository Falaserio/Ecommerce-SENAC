from django.db import models
from django.contrib.auth.models import User

# Modelo de Produto
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    def __str__(self):
        return self.nome

# Modelo de Cliente
class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=250)
    # O cliente pode ser associado a um usuário para login
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

# Modelo de Pedido
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    concluido = models.BooleanField(default=False)
    produtos = models.ManyToManyField(Produto, through='ItemPedido')

# Modelo de Item do Pedido (para múltiplos produtos)
class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)