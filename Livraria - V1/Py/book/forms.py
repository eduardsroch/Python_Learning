from django import forms
from book.models import Livro
from book.models import Cliente
from book.models import Venda
from book.models import ItemVenda


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'genero', 'preco', 'imagem', 'descricao']
        labels = {'titulo':'Título', 'autor':'Autor', 'editora':'Editora', 'genero':'Gênero', 'preco':'Preço', 'imagem':'Imagem', 'descricao':'Descrição'}
        