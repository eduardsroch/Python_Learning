from django.contrib import admin
from book.models import Livro
from book.models import Venda
from book.models import Cliente
from book.models import ItemVenda
from book.models import Cidade
from book.models import Estado
from book.models import Cep
from book.models import Endereco



admin.site.register(Venda)
admin.site.register(Cliente)
admin.site.register(ItemVenda)
admin.site.register(Cidade)
admin.site.register(Estado)
admin.site.register(Cep)
admin.site.register(Endereco)
admin.site.register(Livro)






