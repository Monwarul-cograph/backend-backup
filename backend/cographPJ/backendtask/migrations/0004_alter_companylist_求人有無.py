# Generated by Django 5.0.7 on 2024-07-30 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendtask', '0003_alter_companylist_上場市場名_alter_companylist_代表者_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companylist',
            name='求人有無',
            field=models.IntegerField(verbose_name='求人有無'),
        ),
    ]
