# Generated by Django 3.0.1 on 2020-06-03 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20200603_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultQuestions',
            fields=[
                ('row_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
            ],
        ),
    ]
