# Generated by Django 3.2.6 on 2022-01-09 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regester', '0007_profile1_ref_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile1',
            name='ref_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile1',
            name='referred_by',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]