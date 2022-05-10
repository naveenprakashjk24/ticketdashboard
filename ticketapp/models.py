from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from pandas import notnull



class Incident_Category(models.Model):
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Service_Category(models.Model):
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Status(models.Model):
    name = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Tech_User(models.Model):
    TECHNICIAN = 'TECHNICIAN'
    ENDUSER = "ENDUSER"
    ROLE = [(TECHNICIAN, 'Technician'), (ENDUSER, 'Enduser')]
    name = models.CharField(max_length=200)
    contact_mo = models.IntegerField()
    role =models.CharField(choices=ROLE, default=TECHNICIAN, max_length=15)
    
    def __str__(self):
        return self.name
    
class RequestTicket(models.Model):
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    insident_category = models.ForeignKey(Incident_Category, on_delete=models.CASCADE, blank=True)
    service_category = models.ForeignKey(Service_Category, on_delete=models.CASCADE, blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(Tech_User, on_delete=models.CASCADE, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    county = models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=200)
    
    @property
    def ticket_notes():
        pass
    
    
    def __str__(self):
        return self.subject
    
    
class Notes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    ticket=models.ForeignKey(RequestTicket, on_delete=models.CASCADE)
    note=models.TextField(blank=True, null=True)
    updated_on =  models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated_on', '-created_on']
        
    def __str__(self):
        return self.note[0:50]
    
