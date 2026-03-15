"""
URL configuration for Loya Eye Hospital.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from apps.core.sitemaps import StaticSitemap, TreatmentSitemap, BlogSitemap
from apps.core.views import robots_txt

admin.site.site_header = 'Loya Eye Hospital Admin'
admin.site.site_title = 'Loya Eye Hospital'

sitemaps = {
    'static': StaticSitemap,
    'treatments': TreatmentSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('', include('apps.core.urls')),
    path('treatments/', include('apps.treatments.urls')),
    path('testimonials/', include('apps.testimonials.urls')),
    path('blog/', include('apps.blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
