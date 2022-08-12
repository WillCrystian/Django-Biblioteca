from datetime import datetime
import imp
from pickle import NONE
from django.http import HttpResponse
from django.shortcuts import redirect, render
from autenticacao.models import Usuario
from .models import Livro, Emprestimo, Categoria
from django.conf import settings


# Create your views here.
def home(request):    
    if request.session.get('usuario'):
        livros = Livro.objects.filter(usuario=request.session.get('usuario'))
        status = request.GET.get('status')

        return render(request, 'home.html', {'livros':livros,
                                             'status':status,
                                             'usuario_logado':request.session.get('usuario'),})
    else:
        return redirect('/auth/login/')

def ver_livro(request, id):
    if request.session.get('usuario'):
        livro = Livro.objects.get(id = id)
        status = request.GET.get('status')
        if request.session.get('usuario') == livro.usuario.id:
            emprestado = Emprestimo.objects.filter(nome_livro=livro)     

            return render(request, 'ver_livro.html', {'livro':livro,
                                                      'status':status,
                                                      'emprestado':emprestado,
                                                      'usuario_logado':request.session.get('usuario'),})
        else:
            return redirect('/home/?status=1')
    else:
        return redirect('/auth/login/')

def cadastrar_categoria(request):
    if request.method == "POST":
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        usuario = Usuario.objects.get(id = request.session.get('usuario'))

        if len(categoria.strip()) == 0:
            return HttpResponse('cadastro vazio')

        try:
            cadastro_categoria = Categoria(categoria = categoria,
                                           descricao = descricao,
                                           usuario = usuario)
            cadastro_categoria.save()
            
            return redirect('/home/')          

        except Exception as erro:            
            return redirect('/home/?status=2')
        
def cadastrar_livro(request):
    return HttpResponse("cadastrar_livro")

def excluir_livro(request, id):
    livro = Livro.objects.get(id=id).delete()
    return redirect("/home/")