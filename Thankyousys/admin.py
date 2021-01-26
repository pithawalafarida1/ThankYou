from django.contrib import admin
from Thankyousys.models import Employee
from Thankyousys.models import Badges
from Thankyousys.models import RnR
from Thankyousys.models import Vendor
from Thankyousys.models import EmpUser
from Thankyousys.models import BadgesSentTable

# Register your models here.
class BadgesSenttable(admin.ModelAdmin):
    list_display = ('Sender','badge_title','Receiver',)
admin.site.register(BadgesSentTable)

class EmpUserTable(admin.ModelAdmin):
    list_display = ('username','password','email',)

admin.site.register(EmpUser)

class EmployeeTable(admin.ModelAdmin):
    list_display = ('name','picture','email','dept')

admin.site.register(Employee, EmployeeTable)

class BadgesTable(admin.ModelAdmin):
    list_display= ('badgename', 'badgetype')

admin.site.register(Badges, BadgesTable)

class RnRTable(admin.ModelAdmin):
    list_display=('empsent','badgetype','badgename','message','emprecvd','date')

admin.site.register(RnR, RnRTable)

class VendorTable(admin.ModelAdmin):
    list_display = ('vendorname','vendorcompany','empsent','badgetype','badgename','message','date')

admin.site.register(Vendor, VendorTable)



