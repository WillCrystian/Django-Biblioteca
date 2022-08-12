from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Usuario
from hashlib import sha256

#email: lorena@gmail.com
#senha: 123456

# Create your views here.
def cadastro(request): 
    if request.session.get('usuario'):
        return redirect('/home')
    status = request.GET.get('status')
    return render(request, 'cadastro.html', {'status':status})

def confirma_cadastro(request): 
    if request.method == "GET":
        return render(request, 'cadastro.html')

    if request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        usuario = Usuario.objects.filter(email=email)

        if len(usuario) > 0:            
            return redirect('/auth/cadastro/?status=1') 
        if len(nome.strip()) == 0:           
            return redirect('/auth/cadastro/?status=2')
        if len(email.strip()) == 0:            
            return redirect('/auth/cadastro/?status=3')
        if len(senha.strip()) < 6:           
            return redirect('/auth/cadastro/?status=4')
        if senha != confirmar_senha:            
            return redirect('/auth/cadastro/?status=5')    

        try:
            senha = sha256(senha.encode()).hexdigest()
            usuario = Usuario(usuario=nome,
                            email=email,
                            senha=senha)
            usuario.save()

            return redirect('/auth/cadastro/?status=0')  
        except:
            return redirect('/auth/cadastro/?status=6') 


def login(request):
    if request.session.get('usuario'):
        return redirect('/home')

    status = request.GET.get('status')
    return render(request, 'login.html', {'status':status})

def confirma_login(request):

    if request.method =="GET":
        return redirect('/auth/login')

    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha = sha256(senha.encode()).hexdigest()

        usuario = Usuario.objects.filter(email=email, senha=senha)

        if len(usuario) > 0:
            request.session['usuario'] = usuario[0].id
            return redirect('/home/')
        else:
            return redirect('/auth/login/?status=1')

def sair(request):
    request.session.flush()
    return redirect('/auth/login/')


       
    