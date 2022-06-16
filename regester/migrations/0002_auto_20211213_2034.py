# Generated by Django 3.2.6 on 2021-12-13 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regester', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('std', models.CharField(choices=[('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('CET', 'CET'), ('JEE', 'JEE'), ('NEET', 'NEET'), ('Navodaya Vidyalaya', 'Navodaya Vidyalaya'), ('12 COMBO', '12COMBO')], default='3', max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='std',
            field=models.CharField(choices=[('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('CET', 'CET'), ('JEE', 'JEE'), ('NEET', 'NEET'), ('Navodaya Vidyalaya', 'Navodaya Vidyalaya'), ('12 COMBO', '12COMBO')], default='3', max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.CharField(max_length=150),
        ),
    ]
