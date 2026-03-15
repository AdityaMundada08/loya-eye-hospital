from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Treatment


class TreatmentListView(ListView):
    model = Treatment
    template_name = 'treatments/treatment_list.html'
    context_object_name = 'treatments'
    queryset = Treatment.objects.filter(is_active=True)


class TreatmentDetailView(DetailView):
    model = Treatment
    template_name = 'treatments/treatment_detail.html'
    context_object_name = 'treatment'
    slug_url_kwarg = 'slug'
    queryset = Treatment.objects.filter(is_active=True)
