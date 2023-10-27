# Generated by Django 4.2.6 on 2023-10-27 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_categoria_produto_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdutoFavorito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorito', models.BooleanField(default=False)),
                ('comprador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.comprador')),
                ('produto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.produto')),
            ],
            options={
                'unique_together': {('comprador', 'produto')},
            },
        ),
    ]
