# Generated by Django 4.0.6 on 2022-08-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livro', '0003_alter_livro_data_cadastro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='emprestado',
        ),
        migrations.AddField(
            model_name='livro',
            name='emprestado',
            field=models.BooleanField(default=False),
        ),
    ]
