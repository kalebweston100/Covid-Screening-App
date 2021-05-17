# Generated by Django 3.0.1 on 2020-06-07 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_defaultquestions'),
    ]

    operations = [
        migrations.AddField(
            model_name='savesearch',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='savesearch',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='savesearch',
            name='status',
            field=models.CharField(default='all', max_length=20),
        ),
    ]