from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap

from testpet import settings
from . import views
from .sitemaps import sitemaps

urlpatterns = [
    path('', cache_page(15)(views.IndexView.as_view()), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('addpage/', views.PostAddView.as_view(), name='add_page'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('post/<slug:post_slug>/', views.PostDetailView.as_view(), name='post'),
    path('edit/<slug:slug>/', views.PostUpdateView.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='delete_page'),
    path('category/<slug:cat_slug>/', views.PostCatsView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.PostTagsView.as_view(), name='tag'),
    path(
            "sitemap.xml",
            cache_page(60 * 60 * 24)(sitemap),
            {"sitemaps": sitemaps},
            name="django.contrib.sitemaps.views.sitemap",
        ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
