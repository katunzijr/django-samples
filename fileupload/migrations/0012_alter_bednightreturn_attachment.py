# Generated by Django 5.0.4 on 2024-04-19 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0011_bednightreturn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bednightreturn',
            name='attachment',
            field=models.JSONField(default=dict),
        ),
    ]