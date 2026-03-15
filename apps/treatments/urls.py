from django.urls import path
from . import views

app_name = 'treatments'

urlpatterns = [
    path('', views.TreatmentListView.as_view(), name='treatment_list'),
    path('<slug:slug>/', views.TreatmentDetailView.as_view(), name='treatment_detail'),
]
