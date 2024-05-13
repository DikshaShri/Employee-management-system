from rest_framework import serializers
from app.models import *

#**************************** Serializer for TableEmployee Model ****************************
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableEmployee
        fields = '__all__'

#**************************** Serializer for EmpPerformance Model ****************************
class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpPerformance
        fields = '__all__'
        write_only_fields = ['Overall_Report']
        
#****************** Serializer for update TableEmployee Model specific_field ******************
class EmployeeSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = TableEmployee
        fields = ['first_name','last_name','address','role',]

#**************************** Serializer for TeamMember Model *********************************
class Team(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'