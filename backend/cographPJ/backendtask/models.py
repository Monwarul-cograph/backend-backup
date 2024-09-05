from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import BLANK_CHOICE_DASH


class CompanyList(models.Model):
    _id = models.AutoField(primary_key=True,editable=False)
    # 更新日: DateField with auto_now for auto-updating timestamp
    更新日 = models.DateField(max_length=255, verbose_name='更新日')
    名称 = models.CharField(max_length=255, verbose_name='名称')
    業界_小分類 = models.CharField(max_length=255, verbose_name='業界_小分類', blank=True, null=True)
    求人有無 =  models.CharField(max_length=255,verbose_name='求人有無')
    事業内容 = models.TextField(verbose_name='事業内容')
    所在地 = models.CharField(max_length=255, verbose_name='所在地')
    設立 = models.IntegerField(verbose_name='設立', null=True, blank=True)
    従業員数 = models.IntegerField(verbose_name='従業員数', null=True, blank=True)
    資本金 = models.CharField(max_length=20, verbose_name='資本金', blank=True, null=True)
    企業URL = models.URLField(max_length=1000, verbose_name='企業URL', null=True, blank=True)
    上場市場名 = models.CharField(max_length=255, verbose_name='上場市場名', null=True, blank=True)
    代表者 = models.CharField(max_length=255, verbose_name='代表者', null=True, blank=True)
    平均年齢 = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='平均年齢', null=True, blank=True)
    お問い合わせ先URL = models.URLField(max_length=1000, verbose_name='お問い合わせ先URL', null=True, blank=True)
    代表電話番号 = models.CharField(max_length=20, verbose_name='代表電話番号', null=True, blank=True)
    
    def __str__(self):
        return self.名称
    

class JobList(models.Model):
    _id = models.AutoField(primary_key=True,editable=False)
    company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, related_name='job_list')
    JOB_TITTLE = models.CharField(max_length=255, verbose_name='JOB Tittle')
    JOB_DESCRIPTION = models.CharField(max_length=255, verbose_name='JOB Description')
    LOCATION = models.TextField(verbose_name='Location')

    def __str__(self):
        return self.COMPANY_NAME 

class URLID(models.Model):
    _id = models.AutoField(primary_key=True,editable=False)
    company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, related_name='urls')
    お問い合わせ先URL = models.URLField(max_length=1000, verbose_name='お問い合わせ先URL', null=True, blank=True)

    def __str__(self):
        return self.お問い合わせ先URL

class HomePageID(models.Model):
     _id = models.AutoField(primary_key=True,editable=False)
     company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, related_name='homepage_urls')
     企業URL = models.URLField(max_length=1000, verbose_name='企業URL', null=True, blank=True)

     def __str__(self):
        return self.企業URL

class CEONumberID(models.Model):
    _id = models.AutoField(primary_key=True,editable=False)
    company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, related_name='ceo_numbers')
    代表電話番号 = models.CharField(max_length=20, verbose_name='代表電話番号', null=True, blank=True)

    def __str__(self):
        return self.代表電話番号

class AddressID(models.Model):
     _id = models.AutoField(primary_key=True,editable=False)
     company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, related_name='addresses')
     所在地 = models.CharField(max_length=255, verbose_name='所在地')

     def __str__(self):
        return self.所在地












