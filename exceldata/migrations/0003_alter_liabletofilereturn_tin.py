# Generated by Django 5.0.4 on 2024-04-26 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exceldata', '0002_alter_liabletofilereturn_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liabletofilereturn',
            name='tin',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
