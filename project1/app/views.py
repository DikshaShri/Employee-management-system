from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import *
from django.contrib.auth.hashers import make_password,check_password
from app.models import *
#********************************** Add a record into TableEmployee Model ****************************************************
@api_view([ 'POST'])
def EmployeePost(request): 
     print(request.data)
     success = False
     message = ''
     errors = ''
     try:
        # Create an instance of the EmployeeSerializer with the request data
        employeeSave = EmployeeSerializer(data=request.data)
        # Check if the data provided is valid
        if employeeSave.is_valid(): 
            # Save the employee data to the TableEmployee model
            EmployeeSaveData=employeeSave.save()
            # Encrypt the password before saving it
            EmployeeSaveData.password = make_password(EmployeeSaveData.password)
            EmployeeSaveData.save()
            success = True
            message = "Data Saved successfully."
        else:
            print(employeeSave.errors)
            errors = employeeSave.errors
            message = "Data not saved. Please enter data carefully."
     except Exception as e:
        print(e)
        message="An error occurred while processing the request."
     return JsonResponse({'success':success,'message':message,'errors':errors})
#***************************************** View or read into TableEmployee Models ************************************************
@api_view([ 'GET'])
def GetEmployee(request):
    try:
        # Fetch all records from the TableEmployee model
        EmployeeGet = TableEmployee.objects.all() 
        # Serialize the employee data
        EmployeeSerializerData = EmployeeSerializer(EmployeeGet,many=True)    
        success = True
        # Return the serialized data along with success status
        return JsonResponse({'success':success,'data':EmployeeSerializerData.data})
    except:
        success = False
        Message="Failed to retrieve employee data."
        return JsonResponse({'success':success,'Message':Message})
#************************************************ Delete a employee from TableEmployee Model **************************************
@api_view([ 'DELETE'])
def Empdelete(request,id):
    # Get the record from TableEmployee whose ID matches the one entered.
    delete_data=TableEmployee.objects.filter(id=id) 
    if delete_data:
        # Delete the selected object.
        delete_data.delete()
        success = True
        message = "Deleted successfully."
        return JsonResponse({'success':success,'message':message})
    else:
        success = False
        message = "Please enter a valid ID."
        return JsonResponse({'success':success,'message':message})
    
#*************** Update into TableEmployee Model(specific fields i.e. first_name','last_name','address','role')*************************
@api_view([ 'PUT'])
def Empupdate(request,id):
    try:
        # Get the object from TableEmployee whose id matches the one entered.
        update=TableEmployee.objects.get(id=id) 
        print(update)
        if update:
            # Get updated data for the selected instance/object.
            serializer=EmployeeSerializerUpdate(instance=update,data=request.data) 
            if serializer.is_valid() and serializer.save():
                success = True
                message = "Updated successfully."
                return JsonResponse({'success':success,'message':message})
            else:
                success = False
                message = "Invalid data."
                return JsonResponse({'success':success,'message':message,'errors':serializer.errors})
        else:
            success = False
            message = "Invalid ID."
            return JsonResponse({'success':success,'message':message})
    except Exception as e:
        print(e)

#******************************** Employee Login then view their details***************************************
@api_view(['GET'])
def EmpLogin(request):    
    try:
        data = request.data
        phone = data.get('phone')
        password = data.get('password')
        # Fetching a record from the TableEmployee Model with the phone number entered by the user.
        Get_Employee=TableEmployee.objects.get(phone=phone) 
        # Checking if the entered password matches the saved encrypted password.
        if check_password(password,Get_Employee.password):
            message="Login successful."
             # Serializing the employee data.
            Employee=EmployeeSerializer(instance=Get_Employee)  
            return JsonResponse({'message':message,'data':Employee.data})
        else:
            message="Incorrect password."
            return JsonResponse({'message':message})
    except Exception as e:
        print(e)
        message="Phone number not found."
        return JsonResponse({'message':message})
#******************************* Assign Team Member to TeamLeader(Admin/ HR )************************************
@api_view([ 'POST'])
def AssignTeamLeader(request): 
     success = False
     message = ''
     try:
        personSave = Team(data=request.data)
        data = request.data
        TeamLeader_id = data.get('TeamLeader_id')
        Member_id = data.get('Member_id')
        GetTeamMemberObject = TeamMember.objects.filter(Member_id=Member_id)
        # Check if the member is previously assigned to another team.
        if GetTeamMemberObject :
            message="Member is already assigned to another team."
            return JsonResponse({'success':success,'message':message}) 
        Get_Employee=TableEmployee.objects.all()  
        TL_Valid=False
        Member_Valid=False     
        for employee in Get_Employee:
            # Check if the role of the entered TeamLeader_id is HR or Admin.
            if employee.id==int(TeamLeader_id) and (employee.role=='HR' or employee.role=='Admin'):
                TL_Valid=True              
        for employee in Get_Employee:
             # Check if the role of the entered Member_id is Team_Member.
            if employee.id==int(Member_id) and (employee.role=='Team_Member'):
                Member_Valid=True
        if personSave.is_valid() and TL_Valid and Member_Valid:
            personSave.save()
            success = True
            message = "Data Save successfully."
        else:
            message="Invalid ID or Member ID is already assigned to another team. "
     except Exception as e:
        print(e)
        message="Invalid Data."
     return JsonResponse({'success':success,'message':message})
#************************** Only TeamLeader(HR/Admin) Login (for makingReport) **************************************************** 
@api_view(['GET'])
def TeamLearderLogin(request):
    success = False
    message = ''
    try:
        data= request.data 
        # For login, three fields are required: TeamLeader_id, Member_id, and Password.
        TeamLeader_id= data.get('TeamLeader_id') 
        Member_id=data.get('Member_id')
        Password=data.get('Password')
        Get_Employee=TableEmployee.objects.get(id=TeamLeader_id)
        # Check if the provided password matches the TeamLeader's password
        if check_password(Password,Get_Employee.password):
            try:
                GetTeamMember=TeamMember.objects.get(Member_id=Member_id)
                if GetTeamMember.TeamLeader_id==TeamLeader_id:
                    success=True
                    message="Login Successfully."
                    return JsonResponse({'success':success,'message':message})
                else:
                    message="Please log in with your Team Member ID."
                    return JsonResponse({'success':success,'message':message})
            except:
                message="Member ID does not exist."
                return JsonResponse({'success':success,'message':message})
        else:
            message="Incorrect TeamLeader ID or password."
            return JsonResponse({'success':success,'message':message})
    except Exception as e:
        print(e)
        message="TeamLeader ID does not exist."
        return JsonResponse({'success':success,'message':message})
#*********************************************** Create Employee Performance Table *******************************************
@api_view([ 'POST'])
def PerformancePost(request):
    print(request.data)
    success = False
    message = ''
    try:
        data= request.data
        TeamLeader_id= data.get('TeamLeader_id')
        Member_id=data.get('Member_id')
        Work_Quality=data.get('Work_Quality')
        Work_Quantity=data.get('Work_Quantity')
        Work_Skills=data.get('Work_Skills')
        Team_Work=data.get('Team_Work')
        Achivements=data.get('Achivements')
        performanceSave = PerformanceSerializer(data=request.data) 
        # Get object whose ID matches the entered ID
        Get_emp_performance=EmpPerformance.objects.filter(Member_id=Member_id)
        if Get_emp_performance:
            message="A performance report already exists for this member. If you want to resubmit, please delete the existing report first."
            return JsonResponse({'success':success,'message':message})
        #making model Mutable
        request.data._mutable=True 
        # Function for grade to number conversion 
        def GradeToNumber(grade):  
            if grade=='A':
                return 100
            elif grade=='B':
                return 80
            elif grade=='C':
                return 60
            elif grade=='D':
                return 40
            else:
                return 20 
        # Overall_Report Attribute contains the average number of entered grades  
        request.data['Overall_Report']=(GradeToNumber(Work_Quality)+ GradeToNumber(Work_Quantity)+GradeToNumber(Work_Skills)+GradeToNumber(Team_Work)+GradeToNumber(Achivements))/5
        try:
            # First, check if Member_id and TeamLeader_id are in the same row in the TeamMember model. If true, then save performance.
            Get_TeamMemberObject=TeamMember.objects.get(Member_id=Member_id)
            if Get_TeamMemberObject.TeamLeader_id==TeamLeader_id:
                if performanceSave.is_valid() and performanceSave.save():
                    success=True
                    message="Performance Created Successfully."
                    return JsonResponse({'success':success,'message':message})
                else:
                    print(performanceSave.errors) 
                    message="Details are not valid. Please fill them carefully."
            else:
                message="Please log in with your Team Member ID."
                return JsonResponse({'success':success,'message':message})
        except:
            message="Member ID does not exist."
            return JsonResponse({'success':success,'message':message})    
    except Exception as e:
        print(e)
    return JsonResponse({'success':success,'message':message})
#*********************************************** Get Performance by Member *******************************************
@api_view([ 'GET'])
def GetPerformanceMember(request):
    try:
        data= request.data
        Member_id=data.get('Member_id')
        PerformanceGet = EmpPerformance.objects.get(Member_id=Member_id)
        PerformanceSerializerData = PerformanceSerializer(PerformanceGet)
        ModifiedPerformanceReportObject = {}
        # Retrieve TeamLeader Name
        Get_TeamLeader_data = TableEmployee.objects.filter(id=PerformanceGet.TeamLeader_id)
        Get_TeamLeader_Name = [emp.first_name for emp in Get_TeamLeader_data]
        # Add TeamLeader Name to ModifiedPerformanceReportObject
        ModifiedPerformanceReportObject['TeamLeader_Name'] =Get_TeamLeader_Name[0]
        # Retrieve Member Name
        Get_Member_data = TableEmployee.objects.filter(id=Member_id)
        Get_Member_Name = [emp.first_name for emp in Get_Member_data]
        # Add Member Name to ModifiedPerformanceReportObject
        ModifiedPerformanceReportObject['member_Name'] =Get_Member_Name[0]
        for i,j in PerformanceSerializerData.data.items():
            # Skip id because Django creates it for every model, not needed here
            if i=='id': 
                continue
            ModifiedPerformanceReportObject[i]=j
        success = True
        return JsonResponse({'success':success,'data':ModifiedPerformanceReportObject})
    except Exception as e:
        print(e)
        success = False
        message="Performance report is either not created or the ID is not valid."
        return JsonResponse({'success':success,'message':message})
#*********************************************** Get Performance by TeamLeader *******************************************
@api_view([ 'GET'])
def GetPerformanceTL(request):
    try:
        data= request.data
        TeamLeader_id=data.get('TeamLeader_id')
        # Fetch performance data for the given TeamLeader_id
        GetEpmPerformanceObject = EmpPerformance.objects.filter(TeamLeader_id=TeamLeader_id)
        GetEmployeePerformance=PerformanceSerializer(GetEpmPerformanceObject,many=True)
        
        if GetEpmPerformanceObject:
            newModifiedReport=[]
            for data in GetEmployeePerformance.data:
                newModifiedArray = {}
                # Retrieve TeamLeader Name from TableEmployee
                GetTeam_Leader_data = TableEmployee.objects.filter(id=TeamLeader_id)
                Get_TeamLeader_Name = [emp.first_name for emp in GetTeam_Leader_data]
                newModifiedArray['TeamLeader_Name'] =Get_TeamLeader_Name[0]
                for key,value in data.items():
                    if key=='id':
                        continue
                    newModifiedArray[key]=value
                    if key=='Member_id':
                        # Retrieve Member Name from TableEmployee
                        Get_Member_data = TableEmployee.objects.filter(id=value)
                        Get_Member_Name = [emp.first_name for emp in Get_Member_data]
                        newModifiedArray['Member_Name'] =Get_Member_Name[0]
                newModifiedReport.append(newModifiedArray)
            success = True
            return JsonResponse({'success':success,'data':newModifiedReport})
        else:
            print(e)
            success = False   
            message="No reports found for this Team Leader ID or the ID is invalid. "
            return JsonResponse({'success':success,'message':message})
    except Exception as e:
        print(e)
        success = False   
        message="ID is invalid or No reports found for this Team Leader ID. "
        return JsonResponse({'success':success,'message':message})    
#*********************************************** Delete Performance by Member *******************************************
@api_view([ 'DELETE'])
def Reportdelete(request):
    try:
        data= request.data
        TeamLeader_id= data.get('TeamLeader_id')
        Member_id=data.get('Member_id')
        Get_TeamMember_object=TeamMember.objects.get(Member_id=Member_id)
        # Check if the entered TeamLeader_id and Member_id are in the same row or not
        if Get_TeamMember_object.TeamLeader_id==TeamLeader_id:
            # Get Performance object of the entered Member_id
            delete=EmpPerformance.objects.filter(Member_id=Member_id)
            if delete:
                delete.delete()# Delete object of the entered Member_id
                success = True
                message = "Report deleted successfully."
                return JsonResponse({'success':success,'message':message})
            else:
                success = False
                message = "Report Not Found."
                return JsonResponse({'success':success,'message':message})
        else:
            success = False
            message = "You are not authorized to delete other team members' reports."
            return JsonResponse({'success':success,'message':message})
    except:
        success = False
        message = "Invalid TeamLeader ID or Member ID."
        return JsonResponse({'success':success,'message':message})   