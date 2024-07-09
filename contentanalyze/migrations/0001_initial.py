# Generated by Django 3.2.10 on 2022-06-17 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Muallif',
                'verbose_name_plural': 'Muallif',
            },
        ),
        migrations.CreateModel(
            name='Resurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Resurs',
            },
        ),
        migrations.CreateModel(
            name='Soha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('resursId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resurs_to_soha', to='contentanalyze.resurs')),
            ],
            options={
                'verbose_name': 'Soha',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fayl', models.CharField(max_length=250, unique=True)),
                ('author', models.CharField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('alpha', models.CharField(blank=True, max_length=10, null=True)),
                ('nashr', models.CharField(blank=True, max_length=100, null=True)),
                ('nashrYear', models.CharField(blank=True, max_length=100, null=True)),
                ('miningInfo', models.CharField(max_length=250, unique=True)),
                ('sohaID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='soha_to_hujjat', to='contentanalyze.soha')),
            ],
            options={
                'verbose_name': 'Hujjat',
                'verbose_name_plural': 'Hujjat',
            },
        ),
    ]