# Generated by Django 3.2.6 on 2021-12-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0009_delete_userresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='std',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
