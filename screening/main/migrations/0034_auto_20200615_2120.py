# Generated by Django 3.0.1 on 2020-06-16 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20200613_0811'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='denied',
        ),
        migrations.RemoveField(
            model_name='company',
            name='password',
        ),
    ]
