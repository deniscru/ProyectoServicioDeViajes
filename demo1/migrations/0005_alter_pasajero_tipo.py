# Generated by Django 3.2 on 2021-05-23 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo1', '0004_alter_pasajero_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasajero',
            name='tipo',
            field=models.CharField(choices=[('BASICO', 'BASICO'), ('GOLD', 'GOLD')], max_length=6),
        ),
    ]
