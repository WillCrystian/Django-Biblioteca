from django import template

register = template.Library()

@register.filter
def tempo_emprestimo(v1, v2):    
    if v1 == None:
        return 'Livro emprestado'
    if (v1-v2).days == 0 or (v1-v2).days == 1:
        return f'{(v1-v2).days} dia'
    return (v1-v2).days