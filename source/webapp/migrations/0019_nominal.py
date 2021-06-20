# Generated by Django 2.2 on 2021-06-10 14:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_auto_20210604_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nominal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nominal', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='номинал')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nominals', to='webapp.Country', verbose_name='страна')),
            ],
        ),
    ]
