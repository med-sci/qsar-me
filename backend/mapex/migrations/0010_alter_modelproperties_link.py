# Generated by Django 3.2.7 on 2021-09-28 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapex', '0009_modelproperties_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelproperties',
            name='link',
            field=models.URLField(),
        ),
    ]
