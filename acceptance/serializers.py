"""from django.db.models import fields
from rest_framework import serializers
from acceptance import models


class SignSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sign
        fields= ["id","branch_id","service_id","channel_id"]
        read_only_fealds = ["id", ]

    """