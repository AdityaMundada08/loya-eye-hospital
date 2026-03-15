"""
Treatment and TreatmentFAQ models - each treatment = separate SEO page.
"""
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Treatment(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.TextField(blank=True)
    detailed_description = models.TextField(blank=True,
                                            help_text='What is it?')
    symptoms = models.TextField(blank=True,
                                help_text='Common symptoms (can use bullet points)')
    procedure_details = models.TextField(blank=True,
                                        help_text='Treatment process / why early diagnosis')
    benefits = models.TextField(blank=True)
    why_choose_us = models.TextField(blank=True,
                                     help_text='Why choose this hospital for this treatment')
    featured_image = models.ImageField(upload_to='treatments/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('treatments:treatment_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TreatmentFAQ(models.Model):
    """FAQs per treatment - for each treatment page."""
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'question']
        verbose_name = 'Treatment FAQ'
        verbose_name_plural = 'Treatment FAQs'

    def __str__(self):
        return f'{self.treatment.name}: {self.question[:50]}'
