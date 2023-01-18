# Generated by Django 4.1.5 on 2023-01-16 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tutorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('video_url', models.URLField()),
            ],
            options={
                'verbose_name': 'Tutorial',
                'verbose_name_plural': 'Tutorials',
            },
        ),
    ]
