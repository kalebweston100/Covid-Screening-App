# Generated by Django 3.0.1 on 2020-06-02 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200602_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='boolAnswer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='unsafeAnswer',
            field=models.BooleanField(default=True),
        ),
    ]