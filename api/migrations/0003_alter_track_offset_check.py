# Generated by Django 4.0.6 on 2022-09-15 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_track_offset_check'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='offset_check',
            field=models.CharField(default='na', max_length=500),
        ),
    ]
