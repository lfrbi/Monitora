from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Device, Log, DeviceForm
import datetime
import paramiko
import time
from datetime import datetime
# from .forms import DeviceForm


# View untuk halaman utama
def home(request):
    all_device = Device.objects.all()  # Variabel untuk mendapatkan total perangkat
    cisco_device = Device.objects.filter(vendor="cisco")  # Filter perangkat Cisco
    mikrotik_device = Device.objects.filter(vendor="mikrotik")  # Filter perangkat Mikrotik

    context = {  # Data untuk template [tipe dictionary]
        'all_device': len(all_device),  # Menjumlahkan Total perangkat aktif
        'cisco_device': len(cisco_device),  # Menghitung total perangkat Cisco
        'mikrotik_device': len(mikrotik_device),  # Menghitung total perangkat Mikrotik
    }
    return render(request, 'home.html', context)  # Render halaman dengan data


# View untuk menampilkan list perangkat
def devices(request):
    all_device = Device.objects.all()  # Mengambil data perangkat dari model Device

    context = {  # Data untuk template
        'all_device': all_device,  # Menampilkan semua perangkat
    }


    return render(request, 'devices.html', context)  # Render halaman daftar perangkat


# View untuk konfigurasi perangkat
def configure(request):
    if request.method == 'POST':
        selected_device_id = request.POST.getlist('device')  # Mengambil daftar ID perangkat yang dipilih
        mikrotik_commands = request.POST['mikrotik_command'].splitlines()  # Perintah Mikrotik (split per baris)
        cisco_commands = request.POST['cisco_command'].splitlines()  # Perintah Cisco (split per baris)

        for device_id in selected_device_id:  # Loop untuk setiap ID perangkat
            dev = get_object_or_404(Device, pk=device_id)  # Ambil data perangkat berdasarkan ID

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                # Connect ke perangkat menggunakan SSH
                ssh_client.connect(
                    hostname=dev.ip_address, 
                    username=dev.username, 
                    password=dev.password, 
                    port=dev.ssh_port
                )
                
                # Konfigurasi untuk perangkat Cisco
                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send('conf t\n')
                    for cmd in cisco_commands:  # Kirim perintah Cisco
                        conn.send(cmd + "\n")
                        time.sleep(2)  # Delay untuk setiap perintah
                # Konfigurasi untuk perangkat Mikrotik
                elif dev.vendor.lower() == 'mikrotik':
                    for cmd in mikrotik_commands:  # Kirim perintah Mikrotik
                        ssh_client.exec_command(cmd)
                
                log = Log(target=dev.ip_address, action='Configure', status="Success", Time=datetime.now(), messages="No Error")
                log.save()
            except Exception as e:
                print(f"Error connecting to {dev.hostname}: {e}")
                log = Log(target=dev.ip_address, action='Configure', status="Error", Time=datetime.now(), messages=str(e))
                log.save()
            finally:
                ssh_client.close()

        return redirect('home')  # Redirect ke halaman utama setelah konfigurasi selesai
    
    else:
        devices = Device.objects.all()  # Ambil semua perangkat
        context = {
            'devices': devices,
            'mode': 'Configure',  # Menandakan mode konfigurasi
        }
        # Tambahkan daftar vendor ke context
        vendors = [choice[1] for choice in Device.VENDOR_CHOICES]
        context = {
        'devices': devices,
        'mode': 'Configure',
        'vendors': vendors,  # Kirim daftar vendor
}
        return render(request, 'config.html', context)  # Render halaman konfigurasi perangkat


# View untuk verifikasi konfigurasi perangkat
def verify_config(request):
    if request.method == 'POST':
        result = []
        selected_device_id = request.POST.getlist('device')  # Daftar ID perangkat yang dipilih
        mikrotik_commands = request.POST['mikrotik_command'].splitlines()  # Perintah Mikrotik
        cisco_commands = request.POST['cisco_command'].splitlines()  # Perintah Cisco
        
        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)  # Ambil perangkat berdasarkan ID
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Verifikasi konfigurasi perangkat Mikrotik
                if dev.vendor.lower() == 'mikrotik':
                    for cmd in mikrotik_commands:
                        stdin, stdout, stderr = ssh_client.exec_command(cmd)
                        result.append(f"Result on {dev.ip_address}")
                        result.append(stdout.read().decode())  # Ambil output dari perintah

                # Verifikasi konfigurasi perangkat Cisco
                else:
                    conn = ssh_client.invoke_shell()
                    conn.send('terminal 0\n')
                    for cmd in cisco_commands:
                        result.append(f'Result on {dev.ip_address}')
                        conn.send(cmd + "\n")
                        time.sleep(1)
                        output = conn.recv(65535)
                        result.append(output.decode())  # Ambil output dari perintah
                log = Log(target=dev.ip_address, action='Verify Config', status="Success", Time=datetime.now(), messages="No Error")
                log.save()
            except Exception as e:
                print(f"Error connecting to {dev.hostname}: {e}")
                log = Log(target=dev.ip_address, action='Verify Config', status="Error", Time=datetime.now(), messages=str(e))
                log.save()

        result = '\n'.join(result)  # Gabungkan hasil output menjadi string
        return render(request, 'verify_result.html', {'result': result})  # Render hasil verifikasi
    
    else:
        devices = Device.objects.all()  # Ambil semua perangkat
        context = {
            'devices': devices,
            'mode': 'Verify Config',  # Menandakan mode verifikasi
        }
        return render(request, 'config.html', context)  # Render halaman verifikasi


# View untuk menampilkan log
def log(request):
    logs = Log.objects.all()

    context = {
        'Log': Log
    }

    return render(request, 'log.html', context)

# View untuk halaman dashboard overview
def dashboard_overview(request):
    all_device = Device.objects.all()  # Mengambil data perangkat dari model Device



    context = {  # Data untuk template
        'all_device': all_device,  # Menampilkan semua perangkat
    }

    

    return render(request, 'dashboard_overview.html', context)  # Render halaman daftar perangkat
    
    
def add_device(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            # Validasi: Pastikan IP tidak tercampur antar vendor
            vendor = form.cleaned_data['vendor']
            ip_address = form.cleaned_data['ip_address']

            if Device.objects.filter(vendor=vendor, ip_address=ip_address).exists():
                form.add_error('ip_address', 'This IP Address already exists for the selected vendor.')
            else:
                form.save()
                return redirect('device_list')  # Redirect ke halaman daftar perangkat

    else:
        form = DeviceForm()

    return render(request, 'add_device.html', {'form': form})


def device_list(request):
    devices = Device.objects.all()
    return render(request, 'device_list.html', {'devices': devices})
