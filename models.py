from django.db import models

# Create your models here.


class ipaddres(models.Model):
    ip_address=models.CharField(max_length=20)
    port_number=models.CharField(max_length=20)

def __str__ (self):
    return self.ip_address
