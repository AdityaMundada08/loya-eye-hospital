from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'published_at']
    list_editable = ['is_published']
    prepopulated_fields = {'slug': ('title',)}
