# Generated by Django 4.1.5 on 2023-01-16 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentanalyze', '0006_alter_lugatsoha_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='fayl',
            field=models.FileField(max_length=250, unique=True, upload_to=''),
        ),
    ]
