from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import AppointmentForm
from .models import Doctor, Achievement, FAQ, SiteSetting


def home(request):
    from apps.treatments.models import Treatment
    from apps.testimonials.models import Testimonial

    doctors = Doctor.objects.filter(is_active=True)[:3]
    treatments = Treatment.objects.filter(is_active=True, is_featured=True)[:6]
    if not treatments.exists():
        treatments = Treatment.objects.filter(is_active=True)[:6]
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    if not testimonials.exists():
        testimonials = Testimonial.objects.all()[:6]
    achievements = Achievement.objects.all()[:6]

    return render(request, 'core/home.html', {
        'doctors': doctors,
        'treatments': treatments,
        'testimonials': testimonials,
        'achievements': achievements,
    })


def about(request):
    doctors = Doctor.objects.filter(is_active=True)
    achievements = Achievement.objects.all()
    return render(request, 'core/about.html', {
        'doctors': doctors,
        'achievements': achievements,
    })


def contact(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            site = SiteSetting.get_settings()
            # Email to admin (optional - only if EMAIL is configured)
            if site.email and getattr(settings, 'EMAIL_HOST_USER', None):
                try:
                    send_mail(
                        subject=f'New Appointment Request - {appointment.name}',
                        message=(
                            f'Name: {appointment.name}\n'
                            f'Phone: {appointment.phone}\n'
                            f'Email: {appointment.email}\n'
                            f'Preferred date: {appointment.preferred_date or "Not specified"}\n'
                            f'Message: {appointment.message or "-"}'
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[site.email],
                        fail_silently=True,
                    )
                except Exception:
                    pass
            messages.success(request, 'Thank you! We will contact you shortly.')
            return redirect('core:contact')
    else:
        form = AppointmentForm()
    return render(request, 'core/contact.html', {'form': form})


def location(request):
    return render(request, 'core/location.html')


class FAQListView(ListView):
    model = FAQ
    template_name = 'core/faq.html'
    context_object_name = 'faqs'
    queryset = FAQ.objects.filter(is_active=True)


def robots_txt(request):
    """Simple robots.txt for SEO."""
    lines = [
        'User-agent: *',
        'Allow: /',
        '',
        f'Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def appointment_submit(request):
    """Standalone endpoint for AJAX/form submission from any page."""
    if request.method != 'POST':
        return redirect('core:home')
    form = AppointmentForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Thank you! We will contact you shortly.')
    else:
        messages.error(request, 'Please check your details and try again.')
    next_url = request.GET.get('next') or request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)
