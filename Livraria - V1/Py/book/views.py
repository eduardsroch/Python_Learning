from django.shortcuts import render
from book.models import Livro 
from book.forms import LivroForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def home(request):
    livro = Livro.objects.order_by('livro_id')
    context = {'livro':livro}
    return render(request, 'home.html', context)

def autores(request):
    livro = Livro.objects.order_by('livro_id')
    context = {'livro':livro}
    return render(request, 'autores.html', context)

def fale(request):
    return render(request, 'fale.html')

def imprensa(request):

    if request.method != 'POST':
        form = LivroForm()
    else:
        form = LivroForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))

    context = {'form':form}
    return render(request, 'imprensa.html',context)

def sobre(request):
    return render(request, 'sobre.html')

def titulos(request):
    livro = Livro.objects.order_by('livro_id')
    context = {'livro':livro}
    return render(request, 'titulos.html', context)

def professor(request):
    return render(request, 'professor.html')

def abouteditora(request):
    return render(request, 'abouteditora.html')
