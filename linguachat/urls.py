# 7. URLS CONFIGURATION
# ========================

# linguachat/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from accounts.views import dashboard_view

from django.urls import path, include
from accounts.views import dashboard_view
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_view, name='dashboard'),
    path('accounts/', include('accounts.urls')),
    # Removed duplicate API accounts URLs to avoid routing conflicts
    # path('api/accounts/', include('accounts.urls')),
    path('api/conversations/', include('conversations.urls')),
    path('api/rewards/', include('rewards.urls')),
    path('api/challenges/', include('challenges.urls')),
    path('api/progress/', include('progress.urls')),
    path('api/cultural/', include('cultural_content.urls')),
    path('api/notifications/', include('notifications.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
