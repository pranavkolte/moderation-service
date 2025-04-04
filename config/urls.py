"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.http import JsonResponse
from rest_framework import status
from django.conf import settings
from django.conf.urls.static import static

def healthcheck(request):
    return JsonResponse(
        data={"message": "Moderation API is up and running!"},
        content_type="application/json",
        status=status.HTTP_200_OK,
    )

api_versions = {
    "v1": [
        ("user.auth_urls", "auth/"),
        ("user.user_urls", "user/"),
        ("post.urls", "post/"),
    ]
}



urlpatterns = [
    path('', healthcheck, name='healthcheck'),
    path('admin/', admin.site.urls),
]

for version, routes in api_versions.items():
    for app_url, base_path in routes:
        urlpatterns.append(path(f"api/{version}/{base_path}", include(app_url)))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)