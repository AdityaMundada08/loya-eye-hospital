from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('location/', views.location, name='location'),
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('appointment-submit/', views.appointment_submit, name='appointment_submit'),
]
