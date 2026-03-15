from django.db import models


class Testimonial(models.Model):
    patient_name = models.CharField(max_length=200)
    patient_city = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5,
                                              help_text='1-5')
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.patient_name
