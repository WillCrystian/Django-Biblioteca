# Generated by Django 4.0.6 on 2022-08-16 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0002_remove_emprestimo_usuario_cadastrado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='data_cadastro',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
