# Generated by Django 5.0.4 on 2024-04-18 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0005_alter_mymodel_attachments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='attachments',
            field=models.JSONField(blank=True, null=True),
        ),
    ]