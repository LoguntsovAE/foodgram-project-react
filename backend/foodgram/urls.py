from django.contrib import admin
from django.urls.conf import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('recipe.urls')),
    path('api/', include('users.urls')),
]
