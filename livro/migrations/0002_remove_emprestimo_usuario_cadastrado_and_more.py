# Generated by Django 4.0.6 on 2022-07-19 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacao', '0002_alter_usuario_senha'),
        ('livro', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='usuario_cadastrado',
        ),
        migrations.RemoveField(
            model_name='livro',
            name='emprestado',
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='emprestado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='autenticacao.usuario'),
        ),
        migrations.AddField(
            model_name='livro',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='autenticacao.usuario'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_devolucao',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='data_emprestimo',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emprestimo',
            name='usuario_anonimo',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='livro',
            name='co_autor',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=50)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='autenticacao.usuario')),
            ],
        ),
        migrations.AlterField(
            model_name='livro',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='livro.categoria'),
        ),
    ]
