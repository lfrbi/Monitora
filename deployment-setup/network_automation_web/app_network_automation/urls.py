from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Tambahkan koma setelah path pertama
    path('devices', views.devices, name='devices'),
    path('configure', views.configure, name='configure'),
    path('verify_config', views.verify_config, name='verify_config'),
    path('log', views.log, name='log'),
    path('dashboard_overview', views.dashboard_overview, name='dashboard_overview'),




]
