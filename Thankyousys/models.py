from django.db import models

# Create your models here.

class BadgesSentTable(models.Model):
    Sender = models.CharField(null=True, blank=True, max_length=122)
    badge_title = models.CharField(null=True, blank=True, max_length=122)
    Receiver = models.CharField(null=True, blank=True, max_length=122)
    def __str__(self):
        return self.Receiver

class EmpUser(models.Model):
    username = models.CharField(null=True, blank=True, max_length=122)
    password = models.CharField(null=True, blank=True, max_length=122)
    email = models.CharField(null=True, blank=True, max_length=122)
    def __str__(self):
        return self.username
 
class Employee(models.Model):
    name = models.CharField(null=True, blank=True, max_length=122)
    picture = models.CharField(null=True, blank=True, max_length=122)
    email = models.CharField(null=True, blank=True, max_length=122)
    dept = models.CharField(null=True, blank=True, max_length=122)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Badges(models.Model):
    badgename = models.CharField(null=True, blank=True, max_length=122)
    badgetype = models.CharField(null=True, blank=True, max_length=122)
    def __str__(self):
        return self.badgename

class RnR(models.Model):
    empsent = models.CharField(null=True, blank=True, max_length=122)
    badgetype = models.CharField(null=True, blank=True, max_length=122)
    badgename = models.CharField(null=True, blank=True, max_length=122)
    message = models.CharField(null=True, blank=True, max_length=122)
    emprecvd = models.CharField(null=True, blank=True, max_length=122)
    date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.empsent

class Vendor(models.Model):
    vendorname = models.CharField(null=True, blank=True, max_length=122)
    vendorcompany = models.CharField(null=True, blank=True, max_length=122)
    empsent = models.CharField(null=True, blank=True, max_length=122)
    badgetype = models.CharField(null=True, blank=True, max_length=122)
    badgename = models.CharField(null=True, blank=True, max_length=122)
    message = models.CharField(null=True, blank=True, max_length=122)
    date = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.vendorname

