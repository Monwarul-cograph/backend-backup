# Generated by Django 5.0.7 on 2024-07-31 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendtask', '0004_alter_companylist_求人有無'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('COMPANY_NAME', models.CharField(max_length=255, verbose_name='CompanyName')),
                ('JOB_TITTLE', models.CharField(max_length=255, verbose_name='JobTittle')),
                ('JOB_DESCRIPTION', models.CharField(max_length=255, verbose_name='JObDescription')),
                ('LOCATION', models.TextField(verbose_name='location')),
            ],
        ),
        migrations.AlterField(
            model_name='companylist',
            name='更新日',
            field=models.DateField(max_length=255, verbose_name='更新日'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='求人有無',
            field=models.CharField(max_length=255, verbose_name='求人有無'),
        ),
    ]
