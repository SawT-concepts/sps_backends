# Generated by Django 4.1.5 on 2023-01-16 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='hash',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
