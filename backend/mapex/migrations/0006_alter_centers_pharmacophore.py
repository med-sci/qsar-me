# Generated by Django 3.2.7 on 2021-09-28 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapex', '0005_auto_20210928_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centers',
            name='pharmacophore',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mapex.pharmacophore'),
        ),
    ]
