# Generated by Django 3.2.20 on 2023-08-10 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_getme_help_app', '0004_auto_20230809_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='lattitude',
            field=models.CharField(default=1, max_length=100),
        ),
        migrations.AddField(
            model_name='bookings',
            name='longitude',
            field=models.CharField(default=1, max_length=100),
        ),
        migrations.AddField(
            model_name='worker',
            name='lattitude',
            field=models.CharField(default=1, max_length=100),
        ),
        migrations.AddField(
            model_name='worker',
            name='longitude',
            field=models.CharField(default=1, max_length=100),
        ),
    ]
