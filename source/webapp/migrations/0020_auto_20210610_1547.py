# Generated by Django 2.2 on 2021-06-10 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0019_nominal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nominal',
            name='country',
        ),
        migrations.AddField(
            model_name='nominal',
            name='currency',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='nominals', to='webapp.Currency', verbose_name='валюта'),
        ),
    ]
