from django.contrib import admin
from .models import Testimonial


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'patient_city', 'rating', 'is_featured', 'created_at']
    list_editable = ['is_featured']
