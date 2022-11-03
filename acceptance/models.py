from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
import requests
import json

from requests.api import delete


class Sign(models.Model):
    branch_id = models.IntegerField("Brench Id")
    service_id = models.IntegerField("Service Id")
    channel_id = models.CharField("Channel Id",blank=True,null=True,max_length=150)
  
class PersonalInfo(models.Model):
    full_name = models.CharField("Full Name",blank=True,null=True,max_length=80)
    email = models.CharField("Email",blank=True,null=True,max_length=90)
    gender = models.CharField("Gender",blank=True,null=True,max_length=10)
    age_range = models.CharField("Age Range",blank=True,null=True,max_length=20)
    
    comment = models.CharField("Comment",blank=True,null=True,max_length=1000)


class QmaticLog(models.Model):
    
    branch_id = models.IntegerField("Brench Id")
    service_id = models.IntegerField("Service Id")
    customer_number = models.CharField("Customer Number",blank=True,null=True,max_length=50)
    customer_link = models.CharField("Customer Link",blank=True,null=True,max_length=150)
    transaction_time = models.CharField("Transaction time",max_length=50)
    staff_id = models.CharField("Staff id",max_length=50)
    ticked_id = models.CharField("Ticket id",max_length=70)
    waiting_time = models.CharField("Waiting Time",max_length=70)
    transaction_time = models.CharField("Transaction time",max_length=70)
    personal_info = models.ForeignKey(PersonalInfo,on_delete=models.CASCADE,blank=True,null=True)
    feedback = models.BooleanField(verbose_name="Feedback")

    def save(self,*args, **kwargs):
        obj = Sign.objects.filter(branch_id=self.branch_id,service_id=self.service_id).last()
        try:
            channel_id = obj.channel_id
            self.customer_link = self.find_username(channel_id)[0]
        except:
            pass
        
        super().save(*args, **kwargs)

    @staticmethod
    def find_username(channelId):
        head = {'X-Auth-Token':''}
        req = requests.get('https://api.qmeter.net/v1/branches',headers=head)#headers=head
        print("FINDDD BASLANQIC")
        usernameJson = req.json()
        for i in usernameJson:
            try:
                
                webData=[]
                need = ["name","username","id"]
                if (i.get("accounts")).get("web"):
                    for walk in range(len(i["accounts"]["web"])):
                        copy = []
                        for name in need:
                            copy+=[(i["accounts"]["web"][walk][name])]
                        copy+=[(i["company_id"])]
                        copy+=[(i["accounts"]["web"][walk]["template"]["name"])]
                        copy+=[(i["accounts"]["web"][walk]["template"]["id"])]
                        keys = ["name","username","id","company_id","template_name","template_id"]
                        newDic = dict(zip(keys,copy))
                        
                        webData+=[newDic]
                        
                
                for data in webData:
                    if data.get("id") == channelId:
                        company_id = data.get("company_id")
                        template_id = data.get("template_id")
                        username = data.get("username") # USERNAME BURDA TAPILIR
                        return [username,company_id,template_id] #username
            
            except:
                pass



class ServiceRate(models.Model):
    service_id = models.CharField("Service Id",max_length=1500)
    rate = models.CharField("Rate",max_length=15000)
    qmatic_log = models.ForeignKey(QmaticLog,on_delete=models.CASCADE)
