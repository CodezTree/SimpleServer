# Generated by Django 2.2.4 on 2019-08-18 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_token', models.CharField(max_length=200)),
                ('firebase_token', models.CharField(max_length=200)),
                ('user_sum_temp', models.TextField()),
                ('user_link_temp', models.TextField()),
            ],
        ),
    ]
