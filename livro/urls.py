from django.urls import path
from . import views

urlpatterns = [    
    path('home/', views.home, name='home'),
    path('ver_livro/<int:id>/', views.ver_livro, name='ver_livro'),
    path('cadast_categoria/', views.cadast_categoria, name='cadast_categoria'),
    path('cadastrar_categoria/', views.cadastrar_categoria, name='cadastrar_categoria'),
    path('cadast_livro/', views.cadast_livro, name='cadast_livro'),
    path('cadastrar_livro/', views.cadastrar_livro, name='cadastrar_livro'),
    path('excluir_livro/<int:id>/', views.excluir_livro, name='excluir_livro'),
    path('emprestar_livro/', views.emprestar_livro, name='emprestar_livro'),
    path('devolver_livro/', views.devolver_livro, name='devolver_livro'),
    path('avaliar_livro/', views.avaliar_livro, name='avaliar_livro'),
    path('editar_livro/<int:id>', views.editar_livro, name='editar_livro'),
]