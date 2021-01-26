from rest_framework import serializers
from Thankyousys.models import Employee
from Thankyousys.models import Badges
from Thankyousys.models import RnR
from Thankyousys.models import Vendor
from Thankyousys.models import EmpUser
from Thankyousys.models import BadgesSentTable


class maketableSerializer(serializers.ModelSerializer):
	class Meta:
		model = BadgesSentTable
		fields ='__all__'


class EmpUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmpUser
		fields ='__all__'

class EmployeeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Employee
		fields ='__all__'

class BadgesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Badges
		fields ='__all__'

class RnRSerializer(serializers.ModelSerializer):
	class Meta:
		model = RnR
		fields ='__all__'

class VendorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vendor
		fields ='__all__'