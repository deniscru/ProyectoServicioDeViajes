# Generated by Django 3.2 on 2021-06-26 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo1', '0015_pasajero_fecha_habilitacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='pasajero',
            name='habilitado',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='pasajero',
            name='fecha_habilitacion',
            field=models.DateField(),
        ),
    ]
