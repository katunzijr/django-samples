# Generated by Django 5.0.4 on 2024-04-26 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exceldata', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='liabletofilereturn',
            options={'verbose_name': 'LiableToFileReturn', 'verbose_name_plural': 'LiableToFileReturns'},
        ),
        migrations.AlterModelTable(
            name='liabletofilereturn',
            table='EFILE_LIABLE_TO_FILE_RETURN',
        ),
    ]
