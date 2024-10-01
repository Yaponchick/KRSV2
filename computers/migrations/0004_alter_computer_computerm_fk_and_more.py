# Generated by Django 5.1.1 on 2024-09-19 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0003_remove_motherboard_computerm_fk_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='computerM_FK',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='computers.motherboard', verbose_name='Материнская плата'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='computerPU_FK',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='computers.powerunit', verbose_name='Блок питания'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='computerP_FK',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='computers.processor', verbose_name='Процессор'),
        ),
        migrations.AlterField(
            model_name='computer',
            name='computerV_FK',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='computers.videocard', verbose_name='Видеокарта'),
        ),
    ]
