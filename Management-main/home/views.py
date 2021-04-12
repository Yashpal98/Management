from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Teacher, Student
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import password_changed

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    else:
        return render(request, 'login.html')

def handleLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,"Logged in successfully")
            loginuser = User.objects.get(email=email)
            if(loginuser.is_superuser):
                # return HttpResponse("Hello super User!")
                return redirect("dashboard")

            if(loginuser.is_student):
                return redirect("dashboard")

            if(loginuser.is_teacher):
                return redirect("dashboard")

        else:
            messages.error(request,"Invalid credentials. Please try agian")
            return redirect('home')
    return HttpResponse("404 - Not Found")

def dash(request):
    if request.user.is_authenticated:
        return render(request, 'Dash.html')
    else:
        return redirect("home")
        
@login_required
def Logout(request):
    logout(request)
    return redirect('home')

@login_required
def adminList(request):
    if request.user.is_superuser:
        admin = User.objects.filter(is_superuser=True)
        params = {'users':admin, 'admin':True}
        return render(request, 'list.html', params)
    else:
        return redirect("dashboard")

@login_required
def teacherList(request):
    if request.user.is_superuser or request.user.is_teacher:
        teacher = User.objects.filter(is_teacher=True)
        params = {'users':teacher, 'teacher':True}
        return render(request, 'list.html', params)
    else:
        return redirect("dashboard")

@login_required
def studentList(request):
    if request.user.is_superuser or request.user.is_teacher:
        student = User.objects.filter(is_student=True)
        params = {'users':student, 'student':True}
        return render(request, 'list.html', params)
    else:
        return redirect("dashboard")

@login_required
def deleteUser(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_superuser or user.is_teacher:
        if request.user.is_supeuser:
            user.delete()
            messages.success(request,"Deleted successfull.")
            return redirect("dashboard")
        else:
            messages.warning(request,"You are not authorize to delete this user")
            return redirect("dashboard")
    
    elif user.is_student:
        if request.user.is_superuser or request.user.is_teacher:
            user.delete()
            messages.success(request,"Deleted successfull.")
            return redirect("dashboard")
        else:
            messages.warning(request,"You are not authorize to delete this user")
            return redirect("dashboard")


@login_required
def addAdmin(request):
    if request.user.is_superuser:
        param = {'admin':True}
        if request.method == 'POST':
            fname = request.POST['fname'].upper()
            lname = request.POST['lname'].upper()
            email = request.POST['email']
            password = email + '#' + lname
            users = User.objects.all()

            for user in users:
                if email == user.email:
                    messages.error(request,"Email must be unique!")
                    return redirect("addAdmin")
            if not(all(char.isalpha() or char.isspace() for char in fname)):
                messages.error(request,"First name must be only Letters.")
                return redirect("addAdmin")
        
            if not(all(char.isalpha() or char.isspace() for char in lname)):
                messages.error(request,"Last name must be only Letters.")
                return redirect("addAdmin")

            # Create the User
            adminUser = User.objects.create_user(email, password)
            adminUser.first_name = fname
            adminUser.last_name = lname
            adminUser.is_staff = True
            adminUser.is_superuser = True
            adminUser.save()
            group = Group.objects.get(name="Admin")
            adminUser.groups.add(group)
            messages.success(request,"Admin add Successfully.")
            return redirect("addAdmin")
        return render(request, 'add.html', param)
    else:
        messages.error(request,"You are not authorize to add this user!")
        return redirect("dashboard")

@login_required
def addTeacher(request):
    if request.user.is_superuser:
        param = {'teacher':True}
        if request.method == 'POST':
            fname = request.POST['fname'].upper()
            lname = request.POST['lname'].upper()
            email = request.POST['email']
            teacherId = request.POST['teacherId']
            mobile = request.POST['mobile']
            department = request.POST['department'].upper()
            password = '#' + teacherId + '@' + mobile
            users = User.objects.all()
            teacher = Teacher.objects.all()

            for user in users:
                if email == user.email:
                    messages.error(request,"Email must be unique!")
                    return redirect("addTeacher")
            for user in teacher:
                if teacherId == user.teacher_id:
                    messages.error(request,"Teacher Id must be unique!")
                    return redirect("addTeacher")

            if not(all(char.isalpha() or char.isspace() for char in fname)):
                messages.error(request,"First name must be only Letters.")
                return redirect("addTeacher")
        
            if not(all(char.isalpha() or char.isspace() for char in lname)):
                messages.error(request,"Last name must be only Letters.")
                return redirect("addTeacher")
            
            if not(all(char.isalpha() for char in department)):
                messages.error(request,"Department can not containe Numbers and spaces!")
                return redirect("addTeacher")

            # Create the User
            teacherUser = User.objects.create_user(email, password)
            teacherUser.first_name = fname
            teacherUser.last_name = lname
            teacherUser.is_teacher = True
            teacherUser.save()
            teacher = Teacher.objects.create(user=teacherUser, teacher_id=teacherId, phone_no=mobile, department=department)
            teacher.save()
            group = Group.objects.get(name="Teacher")
            teacherUser.groups.add(group)
            messages.success(request,"Teacher added Successfully.")
            return redirect("addTeacher")

        # return redirect("addTeacher")
        return render(request, 'add.html', param)
    else:
        messages.success(request,"You are not authorize to add this user!")
        return redirect("dashboard")

@login_required
def addStudent(request):
    if request.user.is_superuser or request.user.is_teacher:
        param = {'student':True}
        if request.method == 'POST':
            fname = request.POST['fname'].upper()
            lname = request.POST['lname'].upper()
            email = request.POST['email']
            rollno = request.POST['rollNo']
            mobile = request.POST['mobile']
            course = request.POST['course'].capitalize()
            department = request.POST['department'].upper()
            password = '#$' + rollno + '@%' + mobile
            users = User.objects.all()
            studentch = Student.objects.all()

            for user in users:
                if email == user.email:
                    messages.error(request,"Email must be unique!")
                    return redirect("addStudent")

            for user in studentch:
                if rollno == user.rollno:
                    messages.error(request,"Roll No. must be unique!")
                    return redirect("addStudent")

            if not(all(char.isalpha() or char.isspace() for char in fname)):
                messages.error(request,"First name must be only Letters.")
                return redirect("addStudent")
        
            if not(all(char.isalpha() or char.isspace() for char in lname)):
                messages.error(request,"Last name must be only Letters.")
                return redirect("addStudent")
            
            if not(all(char.isalpha() or char=='.' for char in course)):
                messages.error(request,"Course can not containe Numbers and spaces!")
                return redirect("addStudent")

            if not(all(char.isalpha() for char in department)):
                messages.error(request,"Department can not containe Numbers and spaces!")
                return redirect("addStudent")

            # Create the User
            studentUser = User.objects.create_user(email, password)
            studentUser.first_name = fname
            studentUser.last_name = lname
            studentUser.is_student = True
            studentUser.save()
            student = Student.objects.create(user=studentUser, rollno=rollno, phone_no=mobile, course=course, department=department)
            student.save()
            group = Group.objects.get(name="Student")
            studentUser.groups.add(group)
            messages.success(request,"Student added Successfully.")
            return redirect("addStudent")
        return render(request, 'add.html', param)
    else:
        messages.success(request,"You are not authorize to add this user!")
        return redirect("dashboard")

@login_required
def editAdmin(request, pk):
    user = User.objects.get(pk=pk)
    param = {'user':user, 'admin':True}
    if request.method == 'POST':
        fname = request.POST['fname'].upper()
        lname = request.POST['lname'].upper()
        myuser = User.objects.filter(pk=pk).update(first_name=fname,last_name=lname)
        messages.success(request,"Updated successfully.")
        return redirect("editAdmin", pk=user.id)
    return render(request, 'edit.html', param)

@login_required
def editTeacher(request, pk):
    user = User.objects.get(pk=pk)
    param = {'user':user, 'teacher':True}
    if request.method == 'POST':
        fname = request.POST['fname'].upper()
        lname = request.POST['lname'].upper()
        teacherId = request.POST['teacherId']
        mobile = request.POST['mobile']
        department = request.POST['department'].upper()
        myuser = User.objects.filter(pk=pk).update(first_name=fname,last_name=lname)
        teacher = Teacher.objects.filter(teacher_id=user.teacher.teacher_id).update(teacher_id=teacherId, phone_no=mobile, department=department)

        messages.success(request,"Updated successfully.")
        return redirect("editTeacher", pk=user.id)
    return render(request, 'edit.html', param)

@login_required
def editStudent(request, pk):
    user = User.objects.get(pk=pk)
    param = {'user':user, 'student':True}
    if request.method == 'POST':
        fname = request.POST['fname'].upper()
        lname = request.POST['lname'].upper()
        rollno = request.POST['rollNo']
        mobile = request.POST['mobile']
        course = request.POST['course'].capitalize()
        department = request.POST['department'].upper()
        myuser = User.objects.filter(pk=pk).update(first_name=fname,last_name=lname)
        student = Student.objects.filter(rollno=user.student.rollno).update(rollno=rollno, course=course, phone_no=mobile, department=department)

        messages.success(request,"Updated successfully.")
        return redirect("editStudent", pk=user.id)
    return render(request, 'edit.html', param)

def changePassword(request, pk):
    if request.method == 'POST':
        oldpass = request.POST['oldPassword']
        newpass = request.POST['newPassword']
        repass = request.POST['rePassword']
        user = User.objects.get(pk=pk)
        success = user.check_password(oldpass)
        if not success:
            messages.error(request,"Old password did not match.")
            return redirect("changePassword", pk=user.id)
        if newpass == repass:
            if len(newpass) < 4:
                messages.error(request,"Password length must be equal to or greater than 4 characters.")
                return redirect("changePassword", pk=user.id)
            else:
                messages.success(request,"Password change succesfully.")
                user.set_password(newpass)
                # password_changed(newpass)
                user.save()
                update_session_auth_hash(request, user)
                return redirect("home")
        else:
            messages.error(request,"New Password and Confirm password are different.")
            return redirect("changePassword", pk=user.id)
    return render(request, 'changePassword.html')

def profile(request, pk):
    user = User.objects.get(pk=pk)
    param = {'user':user}
    return render(request, 'profile.html', param)