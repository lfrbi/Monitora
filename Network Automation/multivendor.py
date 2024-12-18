import paramiko
import time

# Fungsi untuk menghubungkan dan mengotomatiskan perangkat Cisco
def connect_to_cisco(hostname, username, password):
    try:
        # Membuat objek SSHClient
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Menghubungkan ke perangkat Cisco
        client.connect(hostname, username=username, password=password)

        # Memulai sesi shell
        remote_conn = client.invoke_shell()

        # Mengirim perintah ke perangkat Cisco
        remote_conn.send("enable\n")
        remote_conn.send("adaptive\n")  # Ganti dengan enable password
        remote_conn.send("configure terminal\n")
        # remote_conn.send("interface gig0/1\n")
        # remote_conn.send("ip address 192.168.1.1 255.255.255.0\n")
        # remote_conn.send("no shutdown\n")
        remote_conn.send("exit\n")
        time.sleep(3)

        # Mengambil dan menampilkan output
        output = remote_conn.recv(65535)
        print(output.decode('utf-8'))

        # Tutup koneksi
        client.close()
    except Exception as e:
        print(f"Error: {e}")

def connect_to_mikrotik(hostname, username, password):
    try: 
        # Membuat objek SSHClient
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Menghubungkan ke perangkat MikroTik
        client.connect(hostname, username=username, password=password)

        # Memulai sesi shell
        remote_conn = client.invoke_shell()

        # Tunggu beberapa detik untuk memastikan sesi shell siap
        time.sleep(3)
        
        # Kirim perintah ke perangkat MikroTik
        remote_conn.send("/ip address add address=192.168.1.2/24 interface=ether4\n")
        remote_conn.send("\n")  # Mengirim newline untuk memastikan prompt kembali
        time.sleep(3)  # Tunggu agar perintah diproses

        # Mengambil dan menampilkan output
        while not remote_conn.recv_ready():  # Tunggu hingga perangkat siap mengirim data
            time.sleep(3)

        output = remote_conn.recv(65535)
        print(output.decode('utf-8'))

        # Tutup koneksi
        client.close()
    except Exception as e:
        print(f"Error: {e}")


# Fungsi utama untuk otomatisasi multivendor
def automate_multivendor(hostname, vendor, username, password):
    if vendor.lower() == "cisco":
        print(f"Connecting to Cisco device at {hostname}...")
        connect_to_cisco(hostname, username, password)
    elif vendor.lower() == "mikrotik":
        print(f"Connecting to MikroTik device at {hostname}...")
        connect_to_mikrotik(hostname, username, password)
    else:
        print("Vendor tidak dikenali!")

# Daftar perangkat yang akan diotomatisasi
devices = [
    {"hostname": "10.10.10.1", "vendor": "cisco", "username": "admin", "password": "adaptive123"},
    {"hostname": "172.11.0.2", "vendor": "mikrotik", "username": "admin", "password": "adaptive"}
]

# Loop untuk otomatisasi beberapa perangkat
for device in devices:
    automate_multivendor(device["hostname"], device["vendor"], device["username"], device["password"])
