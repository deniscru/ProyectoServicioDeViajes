# Generated by Django 3.2 on 2021-05-08 02:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pasajero',
            old_name='fecha_de_Nacimiento',
            new_name='fecha_de_nacimiento',
        ),
    ]
