# Generated by Django 3.0.1 on 2020-06-11 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20200611_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='confirmed',
            new_name='verified',
        ),
    ]
