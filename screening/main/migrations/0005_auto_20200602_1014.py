# Generated by Django 3.0.1 on 2020-06-02 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200602_0921'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saveviewed',
            old_name='entry_id',
            new_name='check_id',
        ),
    ]
