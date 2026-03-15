"""
Core models: SiteSetting, Doctor, Achievement, AppointmentRequest, FAQ.
"""
from django.db import models
from django.utils.text import slugify


class SiteSetting(models.Model):
    """Single-row settings - hospital name, contact, map, hours. No hardcoding."""
    hospital_name = models.CharField(max_length=200)
    tagline = models.CharField(max_length=300, blank=True)
    address = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True,
                                       help_text='Include country code, e.g. 919876543210')
    email = models.EmailField(blank=True)
    google_maps_embed = models.TextField(
        blank=True,
        help_text='Embed code from Google Maps (iframe src or full embed)'
    )
    opening_hours = models.TextField(blank=True,
                                    help_text='e.g. Mon-Sat: 9 AM - 7 PM')
    about_short = models.TextField(blank=True, help_text='Short about for footer/home')
    google_reviews_embed = models.TextField(blank=True,
                                            help_text='Optional: Google reviews widget embed')
    city_name = models.CharField(max_length=100, blank=True,
                                 help_text='e.g. Kolhapur - for "Advanced Eye Care in [City]"')
    meta_title_default = models.CharField(max_length=70, blank=True)
    meta_description_default = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        # Ensure only one row
        if not self.pk and SiteSetting.objects.exists():
            return
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create(
                hospital_name='Loya Eye Hospital',
                city_name='Maharashtra',
            )
        return obj


class Doctor(models.Model):
    """For About page, Home page, SEO credibility."""
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200, blank=True)
    qualification = models.CharField(max_length=300, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Achievement(models.Model):
    """NABH, certifications, awards."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-year']

    def __str__(self):
        return self.title


class AppointmentRequest(models.Model):
    """Lead capture - not full booking. Email + DB entry."""
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.created_at.date()}'


class FAQ(models.Model):
    """General FAQ page - for SEO and AI search (e.g. Is cataract surgery painful?)."""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question)[:300]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.question
