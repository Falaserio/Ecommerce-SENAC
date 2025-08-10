from django import forms
from .models import Produto, Cliente

# Formulário para o modelo de Produto
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']

# Formulário para o modelo de Cliente
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'endereco']

