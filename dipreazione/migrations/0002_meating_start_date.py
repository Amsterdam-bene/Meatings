# Generated by Django 3.0.3 on 2020-02-28 01:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dipreazione', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meating',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
