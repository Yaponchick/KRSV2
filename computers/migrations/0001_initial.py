# Generated by Django 5.1.1 on 2024-09-18 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Motherboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField()),
                ('price', models.TextField()),
                ('compatibleKernels', models.TextField()),
                ('processorPowerConnector', models.TextField()),
                ('supportedMemory', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PowerUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField()),
                ('price', models.TextField()),
                ('networkVoltage', models.TextField()),
                ('coolingSystem', models.TextField()),
                ('power', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField()),
                ('price', models.TextField()),
                ('socket', models.TextField()),
                ('chipset', models.TextField()),
                ('frequency', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VideoСard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField()),
                ('price', models.TextField()),
                ('numberFans', models.TextField()),
                ('turboFrequency', models.TextField()),
                ('memory_size', models.TextField()),
            ],
        ),
    ]
