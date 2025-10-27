from django.contrib import admin
from django.urls import path, include
from events.accounts import signup
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='events/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('', include('events.urls')),
]