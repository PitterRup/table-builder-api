# Generated by Django 4.2.3 on 2023-07-23 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamictable',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
