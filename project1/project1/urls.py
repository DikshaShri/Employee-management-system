"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-employee/',EmployeePost,name='EmployeePost'), #add a record in TableEmployee model
    path('get-employee/',GetEmployee,name='GetEmployee'), #Fetch all record from TableEmployee model
    path('get-delete/<id>',Empdelete,name='Empdelete'), #Delete a record in TableEmployee model
    path('put-update/<id>',Empupdate,name='Empupdate'), #Update a record in TableEmployee model
    path('get-login/',EmpLogin,name='EmpLogin'), #login and view details
    path('post-AssignTeamLeader/',AssignTeamLeader,name='AssignTeamLeader'), #add a record in TeamMember model( for assigning TeamLeader)
    path('teamleader-login/',TeamLearderLogin,name='TeamLearderLogin'),#Login for TeamLeader only for making performance report
    path('create-performance/',PerformancePost,name='PerformancePost'),#add a record in EmpPerformance model
    path('get-performance-Member/',GetPerformanceMember,name='GetPerformanceMember'),#Fetch own performance record by member
    path('get-performance-TeamLeader/',GetPerformanceTL,name='GetPerformanceTL'),#Fetch performance record by TeamLeader
    path('delete-performanceReport/',Reportdelete,name='Reportdelete')#Delete a Performance record by TeamLeader
]
