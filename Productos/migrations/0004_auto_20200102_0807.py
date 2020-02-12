# Generated by Django 2.2.8 on 2020-01-02 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0003_auto_20191220_2102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productogenerico',
            name='unidad_de_medida',
        ),
        migrations.RemoveField(
            model_name='varianteproducto',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='varianteproducto',
            name='pack',
        ),
        migrations.AddField(
            model_name='varianteproducto',
            name='peso_en_kg',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='Peso en Kilogramos'),
        ),
    ]
