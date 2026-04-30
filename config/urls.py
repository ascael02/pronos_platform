from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# drf-spectacular
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path('', include('apps.pronostics.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('bookmakers/', include('apps.bookmakers.urls')),
    path('blog/', include('apps.blog.urls')),
    path('vip/', include('apps.vip.urls')),

    # API
    path('api/v1/', include('apps.api.urls')),

    # Docs (remplacement Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "PronosPlatform Admin"
admin.site.site_title = "PronosPlatform"
admin.site.index_title = "Tableau de bord administrateur"
