from django.db import models

class Device(models.Model):
    ip_address = models.CharField(max_length=255) #tabel ip address
    hostname = models.CharField(max_length=255) #tabel ip hostname
    username = models.CharField(max_length=255) #tabel ip username
    password = models.CharField(max_length=255) #tabel ip password
    ssh_port = models.IntegerField(default=22) #tabel ip port ssh
    

    #models.CharField == string
    #models.IntegerField == integer 
    VENDOR_CHOICES = (('mikrotik', 'Mikrotik'), ('cisco', 'Cisco'))

    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES) #tabel vendor

    def __str__(self):
        return "{}. {}".format(self.id, self.ip_address) #device.id