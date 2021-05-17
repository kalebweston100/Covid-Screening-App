# Generated by Django 3.0.1 on 2020-06-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20200611_0908'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyCompany',
            fields=[
                ('verify_id', models.AutoField(primary_key=True, serialize=False)),
                ('company_id', models.IntegerField()),
                ('url_string', models.TextField(blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Verify',
            new_name='VerifyAccount',
        ),
        migrations.DeleteModel(
            name='Confirm',
        ),
    ]
