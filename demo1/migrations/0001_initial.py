# Generated by Django 3.2 on 2021-05-11 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Combi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=10)),
                ('tipo', models.CharField(choices=[('C', 'Cama'), ('S', 'Semicama')], max_length=1)),
                ('modelo', models.CharField(max_length=40)),
                ('asientos', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Insumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('tipo', models.CharField(max_length=30)),
                ('precio', models.FloatField()),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_de_lugar', models.CharField(max_length=50)),
                ('provincia', models.CharField(max_length=40)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.IntegerField(unique=True)),
                ('telefono', models.BigIntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.TimeField()),
                ('distancia', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('combi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo1.combi')),
                ('destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destino', to='demo1.lugar')),
                ('origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origen', to='demo1.lugar')),
            ],
        ),
        migrations.CreateModel(
            name='Chofer',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='demo1.persona')),
            ],
            bases=('demo1.persona',),
        ),
        migrations.CreateModel(
            name='Pasajero',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='demo1.persona')),
                ('tipo', models.CharField(choices=[('B', 'Basic'), ('G', 'Gold')], max_length=1)),
                ('fecha_de_nacimiento', models.DateField()),
            ],
            bases=('demo1.persona',),
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('precio', models.FloatField()),
                ('asientos', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('insumos', models.ManyToManyField(to='demo1.Insumo')),
                ('ruta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo1.ruta')),
            ],
            options={
                'unique_together': {('ruta', 'fecha')},
            },
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.BigIntegerField(unique=True)),
                ('fecha_de_vencimiento', models.DateField()),
                ('codigo', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('pasajero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo1.pasajero')),
            ],
        ),
        migrations.AddField(
            model_name='combi',
            name='chofer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo1.chofer'),
        ),
    ]
