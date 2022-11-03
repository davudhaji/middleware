from django.shortcuts import render,HttpResponse
import requests
from acceptance import models,serializers

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
import json
# Create your views here.






def example(request):



    obj = models.QmaticLog.objects.filter(feedback=True)
    
    for i in obj:
        print(i)


    










    return render(request,"index2.html",{"obj":obj})

   