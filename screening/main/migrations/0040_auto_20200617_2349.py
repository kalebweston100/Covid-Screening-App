# Generated by Django 3.0.1 on 2020-06-18 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_auto_20200617_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.TextField(),
        ),
    ]
