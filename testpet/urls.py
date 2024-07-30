"""
URL configuration for testpet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from testpet.handlers import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('basefunc.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('users/', include('users.urls', namespace='users')),
    # path('__debug__/', include('debug_toolbar.urls')),
    path('captcha/', include('captcha.urls')),
]

handler404 = page_not_found
if settings.ENABLE_DEBUG_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]