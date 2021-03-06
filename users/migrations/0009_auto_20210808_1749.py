# Generated by Django 3.2.5 on 2021-08-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_profile_new_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='new_mail',
        ),
        migrations.AddField(
            model_name='profile',
            name='mail_edited',
            field=models.CharField(blank=True, default=None, max_length=20000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='new_mail_inbox',
            field=models.CharField(blank=True, default=None, max_length=20000, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='new_mail_outbox',
            field=models.CharField(blank=True, default=None, max_length=20000, null=True),
        ),
    ]
