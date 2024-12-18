from django.db import models
from django import forms

class Device(models.Model):
    ip_address = models.CharField(max_length=255)  # Tabel IP Address
    hostname = models.CharField(max_length=255)    # Tabel Hostname
    username = models.CharField(max_length=255)    # Tabel Username
    password = models.CharField(max_length=255)    # Tabel Password
    ssh_port = models.IntegerField(default=22)     # Tabel SSH Port
    # models.CharField == string
    # models.IntegerField == integer
    
    # Pilihan vendor
    VENDOR_CHOICES = (('mikrotik', 'Mikrotik'), ('cisco', 'Cisco'),)
    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)  # Tabel Vendor

    def __str__(self):
        return "{}. {}".format(self.id, self.ip_address)  # Menampilkan ID dan IP Address perangkat

class Vendor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Log(models.Model):  # Perbaiki models.model menjadi models.Model
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    time = models.DateTimeField(null=True)  # Gunakan DateTimeField untuk waktu
    messages = models.CharField(max_length=255, blank=True)  # Perbaiki typo "messeges" menjadi "messages"

    def __str__(self):
        return "{}. {} - {}".format(self.target, self.action, self.status)

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['ip_address', 'hostname', 'username', 'password', 'ssh_port', 'vendor']

        widgets = {
            'ip_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter IP Address'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Hostname'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
            'ssh_port': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter SSH Port'}),
            'vendor': forms.Select(attrs={'class': 'form-control'}),
        }