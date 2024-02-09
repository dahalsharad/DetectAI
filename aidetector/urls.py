from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import get_text,get_index,get_image,process_text,process_image,get_about



urlpatterns = [
    path('admin/', admin.site.urls),
     path('', get_index, name='index.html'),
    path('text/', get_text, name='text.html'),
    path('index/', get_index, name='index.html'),
    path('image/', get_image, name='image.html'),
    path('about/', get_about, name='about.html'),
    path('process_text/', process_text, name ="process_text"),
    path('process_image/', process_image, name ="process_image"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)