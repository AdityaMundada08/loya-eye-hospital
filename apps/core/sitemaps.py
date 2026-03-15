from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return [
            'core:home',
            'core:about',
            'core:contact',
            'core:location',
            'core:faq',
            'testimonials:testimonial_list',
            'treatments:treatment_list',
        ]

    def location(self, item):
        return reverse(item)


class TreatmentSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        from apps.treatments.models import Treatment
        return Treatment.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        from apps.blog.models import BlogPost
        return BlogPost.objects.filter(is_published=True)

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.updated_at
