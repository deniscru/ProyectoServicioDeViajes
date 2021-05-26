# Generated by Django 3.2 on 2021-05-25 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo1', '0008_auto_20210524_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pasaje',
            name='insumos',
        ),
        migrations.RemoveField(
            model_name='viaje',
            name='insumos',
        ),
        migrations.CreateModel(
            name='CantInsumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('insumo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo1.insumo')),
            ],
        ),
        migrations.AddField(
            model_name='pasaje',
            name='cantInsumos',
            field=models.ManyToManyField(blank=True, to='demo1.CantInsumo'),
        ),
        migrations.AddField(
            model_name='viaje',
            name='cantInsumos',
            field=models.ManyToManyField(blank=True, to='demo1.CantInsumo'),
        ),
    ]