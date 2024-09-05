from django.contrib import admin
from .models import *


@admin.register(CompanyList)
class CompanyModelAdmin(admin.ModelAdmin):
    # 表示するカラムのリスト


  
    list_display = [
        
        '_id ','更新日', '名称', '業界_小分類', '求人有無', '事業内容',
        '所在地', '設立', '従業員数', '資本金',
        '企業URL', '上場市場名', '代表者', '平均年齢','お問い合わせ先URL','代表電話番号'
    ]



@admin.register(JobList)
class JobModelAdmin(admin.ModelAdmin):

    list_display = [
        'COMPANY_NAME',
        'JOB_TITTLE',
        'JOB_DESCRIPTION',
        'LOCATION'
    ]

@admin.register(AddressID)
class AddressModelAdmin(admin.ModelAdmin):

    list_display= [
        'pk','所在地'
    ]

@admin.register(HomePageID)
class HomePageModelAdmin(admin.ModelAdmin):

    list_display = [
       'pk','企業URL'
    ]

@admin.register(URLID)
class URLModelAdmin(admin.ModelAdmin):
    list_display = [
       'pk','お問い合わせ先URL'
    ]

@admin.register(CEONumberID)
class NumberModelAdmin(admin.ModelAdmin):
    list_display = [
        'pk', '代表電話番号'
    ]