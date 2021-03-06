# Generated by Django 2.1.7 on 2019-09-13 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collect_time', models.DateTimeField()),
                ('departure_place', models.CharField(max_length=100)),
                ('departure_time', models.DateTimeField()),
                ('arrival_place', models.CharField(max_length=100)),
                ('line_id', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('delay_time', models.IntegerField()),
            ],
        ),
    ]
