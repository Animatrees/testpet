from django.contrib.sitemaps import GenericSitemap
from .models import Post, Category

posts_info_dict = {
    "queryset": Post.published.all(),
    "date_field": "time_update",
}

cats_info_dict = {
    "queryset": Category.objects.all(),
}

sitemaps = {
    "posts": GenericSitemap(posts_info_dict, priority=0.7, changefreq='weekly'),
    "cats": GenericSitemap(cats_info_dict, priority=0.5, changefreq='weekly'),
}
