from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Tambahkan koma setelah path pertama
    path('devices', views.devices, name='devices'),
    path('configure', views.configure, name='configure'),
    path('verify_config', views.verify_config, name='verify_config'),
    path('log', views.log, name='log'),
    path('dashboard_overview', views.dashboard_overview, name='dashboard_overview'),
    path('get_devices_by_vendor/', views.get_devices_by_vendor, name='get_devices_by_vendor'),

    # path('vendor-selection/', vendor_selection, name='vendor_selection')
    # path('get_ip_by_vendor', views.get_ip_by_vendor, name='get_ip_by_vendor'),
    # path('configure_device', views.configure_device, name='configure_device'),
    # path('input_device_type', views.input_device_type, name='input_device_type'),
    # path('add-device/', views.add_device, name='add_device'),
    # path('device-list/', views.device_list, name='device_list'),
]