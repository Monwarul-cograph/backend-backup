from django.shortcuts import render
from django.http import HttpResponse

# from .models import CompanyList

# Create your views here.
# def AllCompanyList(request):
#     CompaniesList = CompanyList.objects.all()
#     return render(request)


def index(request):
    return HttpResponse('Hi')