# Generated by Django 3.2 on 2021-05-08 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo1', '0004_alter_lugar_activo'),
    ]

    operations = [
        migrations.AddField(
            model_name='combi',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='insumo',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='ruta',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tarjeta',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='viaje',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]
