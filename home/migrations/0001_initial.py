# Generated by Django 4.2.5 on 2023-10-17 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='anonymous', max_length=50)),
                ('email', models.CharField(default='anonymous@.com', max_length=70)),
                ('phone', models.IntegerField(default=0, max_length=15)),
                ('content', models.TextField()),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]