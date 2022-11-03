
from django.db import router
from django.urls import path,include
from acceptance.api.views import SignListView, SignView,SignDelete, QmaticLogView,EncodeLink,MiddlewareFront
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'', SignListView)
router.register(r'qmaticlog/', QmaticLogView)


urlpatterns = [
    
    #path('', SignListView.as_view() , name="SignListView"),
    path('<int:id>/', SignView.as_view() , name="SignView"),
    path('branches/',MiddlewareFront.as_view(),name="branches"),
    path('branches/<int:id>',MiddlewareFront.as_view(),name="branches"),
    path('v1/mwgt/<str:cus>',EncodeLink.as_view(),name="Decode Link")


] + router.urls