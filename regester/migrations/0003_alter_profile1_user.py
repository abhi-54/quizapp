# Generated by Django 3.2.6 on 2021-12-14 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regester', '0002_auto_20211213_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile1',
            name='user',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
