# Generated by Django 4.1.7 on 2023-02-20 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rollingstock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='railvehicle',
            name='id_number',
            field=models.PositiveIntegerField(),
        ),
    ]
