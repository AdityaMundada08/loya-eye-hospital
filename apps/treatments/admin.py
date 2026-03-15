from django.contrib import admin
from .models import Treatment, TreatmentFAQ


class TreatmentFAQInline(admin.TabularInline):
    model = TreatmentFAQ
    extra = 1


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'is_active', 'display_order']
    list_editable = ['is_featured', 'is_active', 'display_order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TreatmentFAQInline]


@admin.register(TreatmentFAQ)
class TreatmentFAQAdmin(admin.ModelAdmin):
    list_display = ['treatment', 'question', 'display_order']
