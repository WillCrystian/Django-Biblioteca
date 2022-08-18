from django import forms
from .models import Categoria, Livro, Emprestimo

class Cadastro_Categoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput() # ocultar informação
        
class Cadastro_Livro(forms.ModelForm):
    class Meta:
        model = Livro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].widget = forms.HiddenInput() # ocultar informação
        self.fields['emprestado'].widget = forms.HiddenInput() # ocultar informação
        
class Emprestimo_Form(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        