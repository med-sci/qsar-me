# Generated by Django 3.2.7 on 2021-09-28 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapex', '0008_auto_20210928_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelproperties',
            name='link',
            field=models.URLField(default=None),
        ),
    ]
