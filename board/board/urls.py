from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from board_data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board_data.urls')),
    path('', include('accounts.urls'))
]
