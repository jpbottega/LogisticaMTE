# Generated by Django 2.2.8 on 2019-12-12 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Movimientos', '0004_auto_20191212_0112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingresosapuntosderecepcion',
            name='distribucion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Movimientos.Distribucion'),
        ),
    ]