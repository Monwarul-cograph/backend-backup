# Generated by Django 5.0.7 on 2024-07-30 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendtask', '0002_rename_backendtask_companylist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companylist',
            name='上場市場名',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='上場市場名'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='代表者',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='代表者'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='企業URL',
            field=models.URLField(blank=True, max_length=1000, null=True, verbose_name='企業URL'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='平均年齢',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=3, null=True, verbose_name='平均年齢'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='従業員数',
            field=models.IntegerField(blank=True, null=True, verbose_name='従業員数'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='更新日',
            field=models.DateField(auto_now=True, null=True, verbose_name='更新日'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='業界_小分類',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='業界_小分類'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='求人有無',
            field=models.IntegerField(blank=True, null=True, verbose_name='求人有無'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='設立',
            field=models.IntegerField(blank=True, null=True, verbose_name='設立'),
        ),
        migrations.AlterField(
            model_name='companylist',
            name='資本金',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='資本金'),
        ),
    ]
