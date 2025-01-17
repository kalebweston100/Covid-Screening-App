# Generated by Django 3.0.1 on 2020-06-11 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_client_denied'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verify',
            fields=[
                ('verify_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('url_string', models.TextField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='client',
            name='email',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.TextField(),
        ),
    ]
