# Generated by Django 3.0.1 on 2020-06-10 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_auto_20200610_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='check_id',
            new_name='check_number',
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='question_id',
            new_name='question_number',
        ),
    ]