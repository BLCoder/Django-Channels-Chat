# Generated by Django 3.0.5 on 2020-04-19 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20200419_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status_up',
            field=models.BooleanField(default=False),
        ),
    ]
