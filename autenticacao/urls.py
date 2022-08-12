from django.urls import include, path
from . import views

urlpatterns = [    
    path('login/', views.login, name='login'),
    path('confirma_login/', views.confirma_login, name='confirma_login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('confirma_cadastro/', views.confirma_cadastro, name='confirma_cadastro'),
    path('sair/', views.sair, name='sair'),
]