# Generated by Django 4.2.6 on 2023-10-15 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_comprador_options_alter_enderecoenvio_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
