# Generated by Django 4.1.7 on 2023-06-14 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rollingstock', '0002_alter_railvehicle_id_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='railvehicle',
            name='location_str',
            field=models.CharField(default="Steve's Mill", max_length=36),
            preserve_default=False,
        ),
    ]