from asyncio import exceptions
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from autenticacao.models import Usuario
from .models import Livro, Emprestimo, Categoria
from .form import Cadastro_Categoria, Cadastro_Livro

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

def cadast_categoria(request):       
    status = request.GET.get('status') 
    if request.session.get('usuario'):
        form = Cadastro_Categoria()
        form.fields['usuario'].initial = request.session.get('usuario')
        
        return render(request, 'cadastrar_categoria.html', {'usuario_logado':request.session.get('usuario'),
                                                            'form':form})                                                        
    return redirect('/home/?status=1')
    
def cadastrar_categoria(request):
    if request.method == "POST":
        if request.session.get('usuario'):
            usuario = request.session.get('usuario')
            form = Cadastro_Categoria(request.POST)
            
            if form.is_valid() and int(usuario) == int(form.data['usuario']):
                form.save()
                return redirect('/home/')
        
            return redirect('/home/?status=2') 
        
def cadast_livro(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session.get('usuario'))
        categorias = Categoria.objects.filter(usuario = usuario)   
        form = Cadastro_Livro()
        
        ### Enviar o id do usuario_logado para o forms ###
        form.fields['usuario'].initial = request.session.get('usuario')
        
        ### Mostrar categorias do usuario logado ###
        form.fields['categoria'].queryset = categorias
        
        return render(request, 'cadastrar_livro.html', {'usuario_logado':request.session.get('usuario'),
                                                        'categorias':categorias,
                                                        'form':form})
    return redirect('/home/?status=1')
        
def cadastrar_livro(request):
    if request.method == "POST":
        if request.session.get('usuario'):
            usuario = request.session.get('usuario')
            form = Cadastro_Livro(request.POST)
            
            if form.is_valid() and int(usuario) == int(form.data['usuario']):
                form.save()
                return redirect('/home/')
            
            return redirect('/home/?status=2')    

def excluir_livro(request, id):
    livro = Livro.objects.get(id=id).delete()
    return redirect("/home/")