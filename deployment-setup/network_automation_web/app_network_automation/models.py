from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=255)  # Tabel IP Address
    hostname = models.CharField(max_length=255)    # Tabel Hostname
    username = models.CharField(max_length=255)    # Tabel Username
    password = models.CharField(max_length=255)    # Tabel Password
    ssh_port = models.IntegerField(default=22)     # Tabel SSH Port
    # models.CharField == string
    # models.IntegerField == integer
    
    # Pilihan vendor
    VENDOR_CHOICES = (('mikrotik', 'Mikrotik'), ('cisco', 'Cisco'))
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)  # Tabel Vendor

    def __str__(self):
        return "{}. {}".format(self.id, self.ip_address)  # Menampilkan ID dan IP Address perangkat


class Log(models.Model):  # Perbaiki models.model menjadi models.Model
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)  # Gunakan DateTimeField untuk waktu
    messages = models.CharField(max_length=255, blank=True)  # Perbaiki typo "messeges" menjadi "messages"

    def __str__(self):
        return "{}. {} - {}".format(self.target, self.action, self.status)
