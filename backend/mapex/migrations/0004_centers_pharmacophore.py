# Generated by Django 3.2.7 on 2021-09-28 11:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapex', '0003_auto_20210916_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Centers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacophore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapex.centers')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mapex.modelproperties')),
            ],
        ),
    ]