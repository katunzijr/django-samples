# Generated by Django 5.0.4 on 2024-04-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0010_alter_multiplefileupload_attachments'),
    ]

    operations = [
        migrations.CreateModel(
            name='BedNightReturn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_master', models.PositiveIntegerField()),
                ('number_of_facility', models.PositiveIntegerField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'BedNightReturn',
                'verbose_name_plural': 'BedNightReturns',
                'db_table': 'EFILE_BNL_RETURN',
            },
        ),
    ]
