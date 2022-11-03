from django.db.models import fields
from rest_framework import serializers
from acceptance.models import Sign,QmaticLog
import requests
import json



class QmaticLogSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = QmaticLog
        fields = [
            'id',
            'branch_id',
            'service_id',
            'transaction_time',
            'customer_number',
            'staff_id',
        ]
    


class SignSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sign
        fields = [
            'id',
            'branch_id',
            'channel_id',
            'service_id',
            
        ]
    




        

        
       