# Generated by Django 4.0.6 on 2022-09-29 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_film_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='film',
            name='highlight',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='film',
            name='language',
            field=models.CharField(default='na', max_length=50),
        ),
        migrations.AddField(
            model_name='film',
            name='other_lang_code',
            field=models.CharField(default='na', max_length=500),
        ),
    ]
