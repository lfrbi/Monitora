from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Device
import paramiko
import time


def home(request):
    all_device = Device.objects.all() # Variabel untuk mendapatkan total 
    cisco_device = Device.objects.filter(vendor="cisco")
    mikrotik_device = Device.objects.filter(vendor="mikrotik")

    context = { # database untuk tamplate [tipe dictionary]
        'all_device': len(all_device),  # Menjumlahkan Total perangkat aktif
        'cisco_device': len(cisco_device), # Menghitung total jumlah perangkat cisco
        'mikrotik_device': len(mikrotik_device), # Menghitung total jumlah perangkat Mikrotik
    }
    return render(request, 'home.html', context) #render fungsi Django yang digunakan untuk menggabungkan template HTML dengan data dari context.


def devices(request):  # Fitur device list
    all_device = Device.objects.all() # variabel untuk mengambil data Device dari class Device pada model.py

    context = {  # database untuk tamplate
        'all_device': all_device, # menampilkan seleuruh
    }

    return render(request, 'devices.html', context)#render fungsi Django yang digunakan untuk menggabungkan template HTML dengan data dari context.

def configure(request):
    if request.method == 'POST':
        selected_device_id = request.POST.getlist('device') # Variabel untuk Mengambil daftar ID perangkat yang dipilih dari data POST
        mikrotik_commands = request.POST['mikrotik_command'].splitlines() # Variabel untuk Mengambil perintah Mikrotik dari data POST dan memisahkannya menjadi list per baris 
        cisco_commands = request.POST['cisco_command'].splitlines() #Variabel untuk Mengambil perintah Mikrotik dari data POST dan memisahkannya menjadi list per baris

        for device_id in selected_device_id: #  Loop akan berjalan untuk setiap ID perangkat dalam selected_device_id
            dev = get_object_or_404(Device, pk=device_id) # Fungsi Django untuk mencari objek di tabel Device berdasarkan device_id (primary key/pk). n Jika data ditemukan: Objek Device (baris data di tabel) akan disimpan dalam variabel dev.

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh_client.connect(
                    hostname=dev.ip_address, 
                    username=dev.username, 
                    password=dev.password, 
                    port=dev.ssh_port
                )
                
                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send('conf t\n')
                    for cmd in cisco_commands: # Melakukan perulangan untuk setiap perintah dalam daftar cisco_commands
                        conn.send(cmd + "\n") # Mengirim perintah konfigurasi ke perangkat melalui saluran interaktif.
                        time.sleep(2)  # Memberikan jeda untuk tiap perintah
                elif dev.vendor.lower() == 'mikrotik': 
                    for cmd in mikrotik_commands:
                        ssh_client.exec_command(cmd)
            except Exception as e:
                print(f"Error connecting to {dev.hostname}: {e}")
            finally:
                ssh_client.close()

        return redirect('home')
    
    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'Configure',
        }
        return render(request, 'config.html', context)
    
# def landing_page_1(request):
        
#         return render(request, 'landing_page_1.html')




# def verify_config(request):
#     if request.method == 'POST':
#         result = []
#         selected_device_id = request.POST.getlist('device')
#         mikrotik_commands = request.POST['mikrotik_command'].splitlines() # Variabel untuk Mengambil perintah Mikrotik dari data POST dan memisahkannya menjadi list per baris 
#         cisco_commands = request.POST['cisco_command'].splitlines() #Variabel untuk Mengambil perintah Mikrotik dari data POST dan memisahkannya menjadi list per baris 
        
#         for x in selected_device_id:
#             dev =get_object_or_404(Device, pk=x)
#             ssh_client = paramiko.SSHClient()
#             ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#             if dev.vendor.lower() == 'mikrotik':
#                 for cmnd in mikrotik_commands:
#                     stdin


























