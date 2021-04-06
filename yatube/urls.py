from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static

handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

urlpatterns = [
    path("about/", include("about.urls", namespace="about")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
