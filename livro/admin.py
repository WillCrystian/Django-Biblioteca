from django.contrib import admin
from .models import Livro, Emprestimo, Categoria

# Register your models here.
admin.site.register(Livro)
admin.site.register(Emprestimo)
admin.site.register(Categoria)