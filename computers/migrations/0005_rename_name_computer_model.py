# Generated by Django 5.1.1 on 2024-09-19 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0004_alter_computer_computerm_fk_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer',
            old_name='name',
            new_name='model',
        ),
    ]
