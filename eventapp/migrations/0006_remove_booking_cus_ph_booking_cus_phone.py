# Generated by Django 5.2 on 2025-06-08 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventapp', '0005_rename_name_booking_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='cus_ph',
        ),
        migrations.AddField(
            model_name='booking',
            name='cus_phone',
            field=models.CharField(default=1, max_length=15, verbose_name='Customer Phone'),
            preserve_default=False,
        ),
    ]
