from django.views.generic import ListView, DetailView
from .models import BlogPost

# For homescreen
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    queryset = BlogPost.objects.filter(is_published=True)

# For detailed view in blogs page
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    queryset = BlogPost.objects.filter(is_published=True)
