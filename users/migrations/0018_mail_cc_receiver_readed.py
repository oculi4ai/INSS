# Generated by Django 3.2.5 on 2021-09-23 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210923_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail_cc_receiver',
            name='readed',
            field=models.BooleanField(default=False),
        ),
    ]
