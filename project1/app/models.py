from django.db import models
#choices for role field in TableEmployee
role=(('Admin','Admin'),
   ('HR','HR'),
   ('Sales','Sales'),
   ('Management','Management'),
   ('Team_Member','Team_Member'),
)
#choices for field used in EmpPerformance
grade=(('A','A'),
   ('B','B'),
   ('C','C'),
   ('D','D'),
   ('E','E'),
)
#creating table in database,to store employee details
class TableEmployee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    phone=models.IntegerField(unique=True)
    role=models.CharField(choices=role, max_length=50)
    password=models.CharField(max_length=100)

#creating table in database,to store employee Performance details
class EmpPerformance(models.Model):
    TeamLeader_id=models.CharField(max_length=50)
    Member_id=models.ForeignKey(TableEmployee, on_delete=models.CASCADE)#making member_id as ForeignKey
    Work_Quality=models.CharField(choices=grade,max_length=50)
    Work_Quantity=models.CharField(choices=grade,max_length=50)
    Work_Skills=models.CharField(choices=grade,max_length=50)
    Team_Work=models.CharField(choices=grade,max_length=50)
    Achivements=models.CharField(choices=grade,max_length=50)
    Overall_Report=models.CharField(max_length=50)
    Remarks=models.CharField(max_length=100)

#creating table in database, to store Team Member assignment details
class TeamMember(models.Model):
    TeamLeader_id=models.CharField(max_length=50)
    Member_id=models.CharField(max_length=50)
