# Generated by Django 3.2.16 on 2023-01-10 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptions',
            name='comment',
            field=models.CharField(db_index=True, default='', max_length=255),
        ),
    ]
