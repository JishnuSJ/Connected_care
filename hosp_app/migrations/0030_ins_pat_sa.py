# Generated by Django 5.0.6 on 2025-05-08 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosp_app', '0029_ins_pat_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='ins_pat',
            name='sa',
            field=models.IntegerField(default=0),
        ),
    ]
