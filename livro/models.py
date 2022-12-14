from distutils.command.upload import upload
from django.db import models
from autenticacao.models import Usuario
from datetime import date

# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__ (self):
        return self.categoria

class Livro(models.Model):
    img = models.ImageField(upload_to='capa_livro', null=True, blank=True )
    nome_livro = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    co_autor = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    data_cadastro = models.DateField(default=date.today)
    emprestado = models.BooleanField(default=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.nome_livro}'

class Emprestimo(models.Model):
    choices = [
        ('B', 'Bom'),
        ('M', 'Médio'),
        ('R', 'Ruim')
    ]
    nome_livro = models.ForeignKey(Livro, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
    usuario_anonimo = models.CharField(max_length=50, blank=True, null=True)
    data_emprestimo = models.DateField(default=date.today)
    data_devolucao = models.DateField(blank=True, null=True)
    avaliacao = models.CharField(max_length=1, choices=choices, default='')
    
    class Meta:
        # ordenar invertido é só colocar o - na frente da variavel
        ordering = ["-data_emprestimo"]
        
    def __str__(self):
        return f'{self.nome_livro} | {self.usuario}'
