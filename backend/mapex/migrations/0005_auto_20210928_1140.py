# Generated by Django 3.2.7 on 2021-09-28 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapex', '0004_centers_pharmacophore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pharmacophore',
            name='center',
        ),
        migrations.AddField(
            model_name='centers',
            name='pharmacophore',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='mapex.pharmacophore'),
            preserve_default=False,
        ),
    ]
