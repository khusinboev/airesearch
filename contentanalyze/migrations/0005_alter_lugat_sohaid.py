# Generated by Django 4.1.5 on 2023-01-15 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contentanalyze', '0004_lugatsoha_lugat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lugat',
            name='sohaID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='soha_to_lugat', to='contentanalyze.lugatsoha'),
        ),
    ]
