# Generated by Django 2.1.3 on 2018-12-08 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playersearch',
            name='aggressionOverFarming',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playersearch',
            name='agressionOverSurvival',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playersearch',
            name='agressionOverVision',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playersearch',
            name='farmingOverSurvival',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playersearch',
            name='farmingOverVision',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='playersearch',
            name='survivalOverVision',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
