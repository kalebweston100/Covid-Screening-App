# Generated by Django 3.0.1 on 2020-06-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20200608_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='key',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='company',
            name='password',
            field=models.CharField(max_length=20),
        ),
    ]