from django.contrib import admin
from .models import SiteSetting, Doctor, Achievement, AppointmentRequest, FAQ


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['hospital_name', 'city_name', 'phone_number', 'whatsapp_number']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'designation', 'experience_years', 'is_active', 'display_order']
    list_editable = ['display_order', 'is_active']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'display_order']
    list_editable = ['display_order']


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'preferred_date', 'is_contacted', 'created_at']
    list_filter = ['is_contacted', 'created_at']
    list_editable = ['is_contacted']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'display_order', 'is_active']
    list_editable = ['display_order', 'is_active']
