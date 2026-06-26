from django.views.generic import ListView
from .models import Testimonial

# The embedded testimonials on home page
class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 12

# Detailed view of testimonials on the testimonials page
