from django.db.models.signals import pre_save ,post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from acceptance.models import QmaticLog
import short_url



@receiver(post_save,sender=QmaticLog)
def check(sender,instance,**kwargs):
    import requests
    user = ''
    password = ''
    phone_number = int(instance.customer_number[1:])
    content = instance.id
    url = short_url.encode_url(int(content))
    re = requests.request('POST', f'http://www.poctgoyercini.com/api_http/sendsms.asp?user={user}&password={password}&gsm={phone_number}&text={url}')
    
    return re.text[6:7]

