# Generated by Django 3.0.1 on 2020-06-11 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20200610_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='key',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='password',
            field=models.TextField(blank=True),
        ),
    ]