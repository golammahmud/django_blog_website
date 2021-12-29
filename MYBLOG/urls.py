
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', users_views.register, name='user_register'),
    path('', include("blog.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)