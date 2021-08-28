# Generated by Django 3.2.5 on 2021-08-14 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20210808_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='icon_path',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='mail_edited',
            field=models.CharField(blank=True, default='[]', max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='new_mail_inbox',
            field=models.CharField(blank=True, default='[]', max_length=20000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='new_mail_outbox',
            field=models.CharField(blank=True, default='[]', max_length=20000, null=True),
        ),
    ]
