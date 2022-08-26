from asyncio import exceptions
from dataclasses import fields
from datetime import datetime, date
from django.http import HttpResponse
from django.shortcuts import redirect, render
from autenticacao.models import Usuario
from .models import Livro, Emprestimo, Categoria
from .form import Cadastro_Categoria, Cadastro_Livro, Emprestimo_Form
from django.contrib.messages import constants
from django.contrib import messages
from django import forms

# Create your views here.
def home(request):
    if request.session.get('usuario'):
        livros = Livro.objects.filter(usuario=request.session.get('usuario'))
        livros_emprestar = Livro.objects.filter(usuario=request.session.get('usuario')).filter(emprestado=False)
        livros_emprestado = Emprestimo.objects.filter(data_devolucao=None)
        todos_usuarios = Usuario.objects.all()       
        
        return render(request, 'home.html', {'livros':livros,
                                             'usuario_logado':request.session.get('usuario'),
                                             'todos_usuarios':todos_usuarios,
                                             'livros_emprestar':livros_emprestar,
                                             'livros_emprestado':livros_emprestado})
    else:
        return redirect('/auth/login/')

def ver_livro(request, id):
    if request.session.get('usuario'):
        livro = Livro.objects.get(id = id)
        livros_emprestar = Livro.objects.filter(usuario=request.session.get('usuario')).filter(emprestado=False)
        livros_emprestado = Emprestimo.objects.filter(data_devolucao=None)
        todos_usuarios = Usuario.objects.all()
        
        
        if request.session.get('usuario') == livro.usuario.id:
            emprestado = Emprestimo.objects.filter(nome_livro=livro)
            
            return render(request, 'ver_livro.html', {'livro':livro,
                                                      'emprestado':emprestado,
                                                      'usuario_logado':request.session.get('usuario'),
                                                      'todos_usuarios':todos_usuarios,
                                                      'livros_emprestar':livros_emprestar,
                                                      'livros_emprestado':livros_emprestado})
        else:
            messages.add_message(request, constants.ERROR, 'Esse Livro não é seu!')
            return redirect('/home/')
    else:

        return redirect('/auth/login/')

def cadast_categoria(request):       
    status = request.GET.get('status') 
    if request.session.get('usuario'):
        form = Cadastro_Categoria()
        form.fields['usuario'].initial = request.session.get('usuario')
        
        return render(request, 'cadastrar_categoria.html', {'usuario_logado':request.session.get('usuario'),
                                                            'form':form})
                                                            
    messages.add_message(request, constants.ERROR, 'Esse Livro não é seu!')                                                  
    return redirect('/home/')
    
def cadastrar_categoria(request):
    if request.method == "POST":
        if request.session.get('usuario'):
            usuario = request.session.get('usuario')
            form = Cadastro_Categoria(request.POST)
            
            # Livro já está cadastrado
            if Categoria.objects.filter(usuario = form.data['usuario']).filter(categoria = form.data['categoria']):
                messages.add_message(request, constants.WARNING, 'Esse livro já está cadastrado')
                return redirect('/home/')
        
            if form.is_valid() and int(usuario) == int(form.data['usuario']):                
                form.save()
                messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso!')
                return redirect('/home/')
            
            messages.add_message(request, constants.ERROR, 'Falha ao cadastrar')
            return redirect('/home/')
    
        
def cadast_livro(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session.get('usuario'))
        categorias = Categoria.objects.filter(usuario = usuario)
        form = Cadastro_Livro()
        
        ### Enviar o id do usuario_logado para o forms ###
        form.fields['usuario'].initial = request.session.get('usuario')
        
        ### Mostrar categorias do usuario logado ###
        form.fields['categoria'].queryset = categorias
        
        ### Enviar o id do usuario_logado para o forms ###
        form.fields['emprestado'].initial = False
        
        return render(request, 'cadastrar_livro.html', {'usuario_logado':request.session.get('usuario'),
                                                        'categorias':categorias,
                                                        'form':form})
        
    messages.add_message(request, constants.ERROR, 'Esse livro não é seu!')
    return redirect('/home/?status=1')
        
def cadastrar_livro(request):
    if request.method == "POST":
        if request.session.get('usuario'):
            usuario = request.session.get('usuario')
            form = Cadastro_Livro(request.POST, request.FILES)
            
            if Livro.objects.filter(usuario = form.data['usuario']).filter(nome_livro = form.data['nome_livro']):
                messages.add_message(request, constants.WARNING, 'Esse livro já está cadastrado')
                return redirect('/home/')
            
            if form.is_valid() and int(usuario) == int(form.data['usuario']):
                form.save()
                messages.add_message(request, constants.SUCCESS, 'Livro cadastrado com sucesso!')
                return redirect('/home/')
            
            messages.add_message(request, constants.ERROR, 'Falha ao cadastrar!')
            return redirect('/home/')

def excluir_livro(request, id):
    livro = Livro.objects.get(id=id).delete()
    return redirect("/home/")

def emprestar_livro(request):
    if request.method == "POST":
        nome_livro = request.POST.get('nome_livro')
        usuario = request.POST.get('usuario')
        usuario_anonimo = request.POST.get('usuario_anonimo')
        
        if Livro.objects.filter(usuario = request.session.get('usuario')).filter(id=nome_livro).filter(emprestado=False):
            if usuario_anonimo == None:
                emprestimo = Emprestimo(nome_livro = Livro.objects.get(id = nome_livro),
                                        usuario = Usuario.objects.get(id = usuario))
            else:
                emprestimo = Emprestimo(nome_livro = Livro.objects.get(id = nome_livro),
                                        usuario_anonimo = usuario_anonimo)
            
            livro = Livro.objects.get(id=nome_livro)
           
            livro.emprestado = True
            livro.save()
            emprestimo.save()   
            
            messages.add_message(request, constants.SUCCESS, 'Livro emprestado com sucesso')
            return redirect('/home/')
        else:
            messages.add_message(request, constants.ERROR, 'Você está tentando acessar livro de outro usuário')
            return redirect('/home/')
        
def devolver_livro(request):
    if request.method == "POST":
        id_emprestimo = request.POST.get('id_emprestado')
        
        emprestimo = Emprestimo.objects.get(id = id_emprestimo)
        emprestimo.data_devolucao = date.today()
        print(emprestimo.nome_livro)
        
        livro = Livro.objects.get(nome_livro = emprestimo.nome_livro)
        livro.emprestado = False
       
        emprestimo.save()
        livro.save()
    
        messages.add_message(request, constants.SUCCESS, 'Livro devolvido com sucesso')
        return redirect(f'/ver_livro/{livro.id}')
    
def avaliar_livro(request):
    if request.method == "POST":
        id_emprestimo = request.POST.get('id_emprestimo')
        id_livro = request.POST.get('id_livro')
        avaliacao = request.POST.get('avaliacao')
        
        emprestimo = Emprestimo.objects.get(id = id_emprestimo)
        emprestimo.avaliacao = avaliacao
        emprestimo.save()
        
        messages.add_message(request, constants.SUCCESS, 'Avaliação efetuada com sucesso')
        return redirect(f'/ver_livro/{id_livro}/')
    
def editar_livro(request, id):
    if request.method == "GET":
        livro = Livro.objects.get(id = id)
        categorias = Categoria.objects.filter(usuario = request.session.get('usuario'))
       
        return render(request, 'editar_livro.html',{'livro':livro,
                                                    'categorias':categorias})
    elif request.method == "POST":
        livro = Livro.objects.get(id = id)
        
        nome_livro = request.POST.get('nome_livro')
        autor = request.POST.get('autor')
        co_autor = request.POST.get('co_autor')
        id_categoria = request.POST.get('id_categoria')
        print(id_categoria)
        categoria = Categoria.objects.get(id= id_categoria)
        print(categoria)
        
        livro.nome_livro = nome_livro
        livro.autor = autor
        livro.co_autor = co_autor
        livro.categoria = categoria
        livro.save()

        return redirect(f'/editar_livro/{livro.id}')
        