from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout/password reset
    path("accounts/", include("events.accounts_urls")),      # signup
    path("", RedirectView.as_view(pattern_name="events:list", permanent=False)),
    path("events/", include(("events.urls", "events"), namespace="events")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
