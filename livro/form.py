from django import forms
from .models import Categoria, Livro

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