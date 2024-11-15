from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from sitewomen import settings

urlpatterns = [
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace="users")),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls'))
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"