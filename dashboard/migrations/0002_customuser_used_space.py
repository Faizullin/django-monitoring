# Generated by Django 4.1.7 on 2023-04-15 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='used_space',
            field=models.FloatField(default=0, verbose_name='used space'),
        ),
    ]
