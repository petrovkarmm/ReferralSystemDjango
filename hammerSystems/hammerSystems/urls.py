from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    path('auth/', include('api_auth_user.urls')),
]
