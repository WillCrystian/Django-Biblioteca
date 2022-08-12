from datetime import datetime
import imp
from pickle import NONE
from django.http import HttpResponse
from django.shortcuts import redirect, render
from autenticacao.models import Usuario
from .models import Livro, Emprestimo, Categoria
from django.conf import settings
from .form import Cadastro_Categoria, Cadastro_Livro

# Create your views here.
def home(request):    
    if request.session.get('usuario'):
        livros = Livro.objects.filter(usuario=request.session.get('usuario'))
        status = request.GET.get('status')
        form_categoria = Cadastro_Categoria()
        form_livro = Cadastro_Livro()
        return render(request, 'home.html', {'livros':livros, 
                                             'status':status, 
                                             'usuario_logado':request.session.get('usuario'),
                                             'form_categoria':form_categoria,
                                             'form_livro':form_livro})
    else:
        return redirect('/auth/login/')

def ver_livro(request, id):
    if request.session.get('usuario'):
        livro = Livro.objects.get(id = id)
        if request.session.get('usuario') == livro.usuario.id:        
            emprestado = Emprestimo.objects.filter(nome_livro=livro)     

            print(emprestado)
            return render(request, 'ver_livro.html', {'livro':livro, 
                                                      'emprestado':emprestado,
                                                      'usuario_logado':request.session.get('usuario'),})
        else:
            return redirect('/home/?status=1')
    else:
        return redirect('/auth/login/')

def cadastrar_categoria(request):
    if request.method == "POST":
        form_categoria = Cadastro_Categoria(request.POST)        

        if form_categoria.is_valid():
            categoria = form_categoria.data['categoria']
            descricao = form_categoria.data['descricao']
            c = Categoria(categoria=categoria,
                                  descricao=descricao,
                                  usuario=int(request.session.get('usuario')))
            c.save()

            
            
            
            return HttpResponse('ok')
        else:
            return redirect('/home/?status=2')

def cadastrar_livro(request):
    return HttpResponse("cadastrar_livro")

def excluir_livro(request, id):
    livro = Livro.objects.get(id=id).delete()
    return redirect("/home/")
    
    

