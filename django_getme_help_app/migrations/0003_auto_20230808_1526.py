# Generated by Django 3.2.20 on 2023-08-08 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_getme_help_app', '0002_chat_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='LOGIN',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='django_getme_help_app.login'),
        ),
        migrations.AddField(
            model_name='worker',
            name='LOGIN',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='django_getme_help_app.login'),
        ),
    ]
