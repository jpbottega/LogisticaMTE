# Generated by Django 2.2.8 on 2020-02-12 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0004_auto_20200102_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='varianteproducto',
            name='peso_en_kg',
        ),
        migrations.AddField(
            model_name='productogenerico',
            name='unidad_de_medida',
            field=models.CharField(choices=[('Kilo', 'Kilogramos'), ('Litro', 'Litros'), ('Unidad', 'Unidad')], default='', max_length=15),
        ),
        migrations.AddField(
            model_name='varianteproducto',
            name='cantidad',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=5, verbose_name='Cantidad por unidad'),
        ),
        migrations.AddField(
            model_name='varianteproducto',
            name='pack',
            field=models.PositiveIntegerField(default=1, verbose_name='Unidades de empaque'),
        ),
    ]
