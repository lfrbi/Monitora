from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),  # Tambahkan koma setelah path pertama
    path('devices', views.devices),
    path('configure', views.configure),
    # path('landing_page_1', views.landing_page_1)
    # path('verify_config', views.verify_config)
]
