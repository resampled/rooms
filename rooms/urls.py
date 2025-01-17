from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.views.static import serve
import webapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('webapp.urls'))
]
