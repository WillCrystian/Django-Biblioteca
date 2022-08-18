from asyncio import exceptions
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from autenticacao.models import Usuario
from .models import Livro, Emprestimo, Categoria
from .form import Cadastro_Categoria, Cadastro_Livro, Emprestimo_Form
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def home(request):
    if request.session.get('usuario'):
        livros = Livro.objects.filter(usuario=request.session.get('usuario'))
        emprestimo_form = Emprestimo_Form()
        emprestimo_form.fields['nome_livro'].queryset = livros
        
        return render(request, 'home.html', {'livros':livros,
                                             'usuario_logado':request.session.get('usuario'),
                                             'emprestimo_form':emprestimo_form})
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
            form = Cadastro_Livro(request.POST)
            
            if Livro.objects.filter(usuario = form.data['usuario']).filter(nome_livro = form.data['nome_livro']):
                messages.add_message(request, constants.WARNING, 'Esse livro já está cadastrado')
                return redirect('/home/')
            
            if form.is_valid() and int(usuario) == int(form.data['usuario']):
                form.save()
                messages.add_message(request, constants.SUCCESS, 'Cadastrado com sucesso!')
                return redirect('/home/')
            
            messages.add_message(request, constants.ERROR, 'Falha ao cadastrar!')
            return redirect('/home/')    

def excluir_livro(request, id):
    livro = Livro.objects.get(id=id).delete()
    return redirect("/home/")