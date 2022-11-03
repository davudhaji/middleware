from django.db.models import query
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from acceptance.api.serializers import SignSerializers,QmaticLogSerializers
from rest_framework.generics import ListAPIView,DestroyAPIView , RetrieveAPIView 
from rest_framework.viewsets import ModelViewSet
from acceptance.models import Sign, QmaticLog,ServiceRate,PersonalInfo
from rest_framework.views import APIView
import requests
import json
from rest_framework.response import Response
import short_url
from rest_framework.permissions import IsAuthenticated, AllowAny
from requests.auth import HTTPBasicAuth



class SignListView(ModelViewSet):
    queryset = Sign.objects.all()
    serializer_class = SignSerializers
    def create(self,request):
        print(request.POST)


class QmaticLogView(ModelViewSet):
    queryset = QmaticLog.objects.all()
    serializer_class = QmaticLogSerializers



class MiddlewareFront(APIView):
    permission_classes = [AllowAny]

    def get(self,request,*args, **kwargs):
        
        if kwargs.get("id"):
            branch_id = kwargs["id"]
            req = requests.get(f'http://ip/{branch_id}/services/',auth=HTTPBasicAuth('', ''))#headers=head
            return Response(req.json())
        
        req = requests.get('http://ip:8080/qsystem/rest/entrypoint/branches/',auth=HTTPBasicAuth('', ''))#headers=head
        
        
       
        return Response(req.json())

    def post(self,request,*args, **kwargs):
        
        print(kwargs)

        print(args)
        #received_json_data = json.loads(request.body)
        #print(received_json_data)
        print(self.request.data)
        return Response({"tosu":"opur"})






class EncodeLink(APIView):

    permission_classes = [AllowAny]
    queryset = Sign.objects.all()
    serializer_class = SignSerializers

    def post(self,request,*args, **kwargs): #867nv
        link_decode = short_url.decode_url(kwargs["cus"])
        obj = QmaticLog.objects.filter(id=link_decode).first()
        if obj.feedback:
            return Response(data={"feedback":True})

        dic = request.data

        
        contact_info = dic.get("contactInfo")
        print(contact_info,"COONRTTTAACCTT")
        new_personal = PersonalInfo()
        new_personal.full_name = contact_info[0].get("fieldValue")
        new_personal.email = contact_info[2].get("fieldValue")
        new_personal.gender = contact_info[3].get("fieldValue")
        new_personal.age_range = contact_info[4].get("fieldValue")
        new_personal.comment = dic.get("comment")
        new_personal.save()
        
        obj.personal_info =  new_personal
        obj.feedback = 1
        obj.save()

        rates = dic.get("rates")
        
        for rate in rates:
            new_rate = ServiceRate()
            new_rate.service_id = rate.get("service_id")
            new_rate.rate = rate.get("rate")
            new_rate.qmatic_log = obj
            new_rate.save()

    

        customer_number = obj.customer_number
        
        username = obj.customer_link #"QLKv1O" 
        dic['contactInfo'][1].update({'fieldName':'phone','fieldValue':customer_number})
        
       
        
        head = {'X-Auth-Token':''}
        
        req = requests.post(f'https://api.qmeter.net/v1/webwidget/{username}',headers=head,json=dic)#headers=head

        return Response(data=req.json())

    def get(self,*args, **kwargs):
        link_decode = short_url.decode_url(kwargs["cus"])
        obj = QmaticLog.objects.filter(id=link_decode).first()
        self.customer_number = obj.customer_number
        channel_id = Sign.objects.filter(branch_id=obj.branch_id,service_id=obj.service_id).last()      
        self.channel_id = channel_id.channel_id
        self.data = QmaticLog.find_username(self.channel_id) #self.find_username(self.channel_id)
        jsn = self.find_json(self.data[0])
        end = self.find_personal_info(self.customer_number,self.data[1],jsn,self.data[2])
        
        return Response(end)
    
    def find_json(self,username):
        jsn = requests.get("https://api.qmeter.net/v1/webwidget/"+username)
        jsn_1 = jsn.json()
        
        return jsn_1
    
    def find_username(self,channelId):
        head = {'X-Auth-Token':''}
        req = requests.get('https://api.qmeter.net/v1/branches',headers=head)#headers=head

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


    


    def find_personal_info(self,number,company_id,jsn,template_id):
            
            import psycopg2
            conn = psycopg2.connect(host="", database="", user="",
                                    password="", port="16435")
            query = f"SELECT id, name, email, phone, permission, company_id, gender, age_range, deleted, created_at, updated_at FROM public.customers where phone ='{number}' and company_id ='{company_id}' ;"
            cur= conn.cursor()
            cur.execute(query)
            personal_info = cur.fetchall()
            if personal_info[0]:
                customer_id = personal_info[0][0]
                full_name = personal_info[0][1]
                email = personal_info[0][2]
                phone_number = personal_info[0][3]
                gender = personal_info[0][6]
                age_range = personal_info[0][7]
                jsn.update({"customer": {"id":customer_id,"name":full_name,"email":email,"phone":phone_number,"gender":gender,"age_range":age_range,"company_id":company_id,"permisson":False}})
                jsn.update({"link":{"cutomerID":customer_id,"templateID":template_id,"company_id":company_id}})
                
                jsn.pop("properties")
               

                return jsn
            return jsn
    

class SignView(RetrieveAPIView):
    queryset = Sign.objects.all()
    serializer_class = SignSerializers
    lookup_field = 'id'

    
class SignDelete(DestroyAPIView):
    queryset = Sign.objects.all()
    serializer_class = SignSerializers
    lookup_field = 'id'

    


