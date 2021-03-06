# Generated by Django 2.2.6 on 2019-12-01 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Movimientos', '0003_auto_20191130_2158'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportacionLineaIngreso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.FileField(upload_to='')),
                ('ingreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Movimientos.IngresosAPuntosDeRecepcion')),
            ],
            options={
                'verbose_name': 'Importacion Linea de Egreso',
                'verbose_name_plural': 'Importacion Lineas de Egreso',
            },
        ),
    ]
