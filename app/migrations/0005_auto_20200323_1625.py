# Generated by Django 3.0.3 on 2020-03-23 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200306_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower_info',
            name='created_at',
            field=models.DateField(default='1234-01-02'),
        ),
        migrations.AlterField(
            model_name='friend_info',
            name='created_at',
            field=models.DateField(default='1234-01-02'),
        ),
    ]