from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("Api.urls")),
    path('payment/', include("Payments.urls")),
    path('s-admin/', include ("s_admin.urls")),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
