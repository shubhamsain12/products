from django.urls import path
from .views import Translate,getAllLanguages,download_pdf,generate_All_pdf,SubscribeView, about, home, contact
from . import views


urlpatterns = [
    #path('', index, name='index'),
    path('', Translate, name='translate'),
    path('getAllLanguages/',getAllLanguages, name='getAllLanguages'),
    # path('download-pdf/<str:param1>/', download_pdf, name='download_pdf'),

    path('download-pdf/<str:param1>/', views.download_pdf, name='download_pdf'),
    path('generate_all_pdf/', views.generate_All_pdf, name='generate_all_pdf'),

    # path('generate_All_pdf/',generate_All_pdf, name='generate_All_pdf'),
    path('email/',SubscribeView.as_view(), name='SubscribeView'),
    path('about/',about),
    # path('home/',home),
    path('contact/',contact)
    
]