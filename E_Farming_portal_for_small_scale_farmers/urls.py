from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_application.urls')),  # include your app routes
]

# Serve static & media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'main_application.views.custom_404'
handler500 = 'main_application.views.custom_500'
handler403 = 'main_application.views.custom_403'
handler400 = 'main_application.views.custom_400'


