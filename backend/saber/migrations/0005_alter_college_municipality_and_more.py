# Generated by Django 5.1 on 2024-09-17 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saber', '0004_alter_college_municipality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='college',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colleges', to='saber.municipality'),
        ),
        migrations.AlterField(
            model_name='highschool',
            name='municipality',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='highschools', to='saber.municipality'),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='municipalities', to='saber.department'),
        ),
    ]
