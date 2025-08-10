from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Produto, Cliente

# Formulário para o registro de clientes comuns
# (o Cliente está associado ao User)
class RegistroForm(UserCreationForm):
    # Campos adicionais para o modelo Cliente
    email = forms.EmailField(label="E-mail")
    telefone = forms.CharField(max_length=20, label="Telefone")
    endereco = forms.CharField(max_length=200, label="Endereço")

    class Meta(UserCreationForm.Meta):
        # A herança de UserCreationForm.Meta já inclui os campos do User
        # Os campos do UserCreationForm são 'username', 'password', 'password2'
        fields = UserCreationForm.Meta.fields + ('email', 'telefone', 'endereco',)
        # Para evitar o erro "Unknown field(s) (username) specified for Cliente"
        # Precisamos garantir que o `Meta.model` seja o User, não o Cliente.
        # No entanto, a forma como o UserCreationForm funciona já é a correta.
        # O erro real pode estar na sua `views.py` na hora de salvar, onde
        # você está tentando passar 'username' para o `Cliente.objects.create`
        # que não tem esse campo.
        
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

# Novo formulário para o registro de usuários administradores
# Este formulário cria um User que é automaticamente um superusuário.
class AdminRegistroForm(UserCreationForm):
    # O email é um campo obrigatório para admins também
    email = forms.EmailField(label="E-mail")

    class Meta(UserCreationForm.Meta):
        # Este formulário não está associado ao modelo Cliente, apenas ao User.
        fields = ('username', 'email', 'password', 'password2')
