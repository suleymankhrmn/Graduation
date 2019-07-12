from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .forms import SingUpForm
from .forms import StudentForm
from .forms import TeacherForm
from .models import Student
from .models import User
from .models import Teacher
from .models import Attendance

from django.contrib.auth.models import Group
# Create your views here.


def detail(request, username):
    attendance_list = Attendance.objects.all()
    attendance_list1 = Attendance.objects.all()
    start_date = request.GET.get('sd')
    finish_date =request.GET.get('fd')

    start_date1 = request.GET.get('sd1')
    finish_date1 = request.GET.get('fd1')
    select_lesson = request.GET.get('sl')
    select_classroom = request.GET.get('cl')
    if start_date1 and finish_date1 and select_classroom:
        attendance_list1 = attendance_list1.filter(attendance_date__range=[start_date1, finish_date1], teacher_id=username, classroom=select_classroom)
    if start_date and finish_date or select_lesson:
        attendance_list = attendance_list.filter(attendance_date__range=[start_date, finish_date], lessons=select_lesson, student_id=username)
    try:
        users = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("Student doesnt not exist")
    return render(request, 'detail.html', {'users': users, 'attendance_list': attendance_list, 'attendance_list1': attendance_list1 })



def studentaffair(request):
    students = Student.objects.all()
    teachers = Teacher.objects.all()
    return render(request, 'studentaffair/controller.html', {'students': students, 'teachers': teachers} )


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        #result = user.groups.filter(name='Students').exists()
        #if result:
        return redirect('pages:studentaffair')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('pages:login')


def singup(request):
    form = SingUpForm(request.POST or None)
    slc = request.POST.get('select')
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        #group = Group.objects.get(name=group1)
        #user.groups.add(group)
        login(request, user)

        if slc == "Student":
            return redirect('pages:stdcreate')
        else:
            return redirect('pages:tchcreate')
    else:
        form = SingUpForm()
        print("jdj")

    return render(request, 'singup.html', {'form': form})


def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save(commit=False)
        student.user = request.user
        student.save()
        return redirect('pages:studentaffair')
    context = {
        'form': form,

    }
    return render(request, 'student_create.html', context)


def teacher_create(request):
    form = TeacherForm(request.POST or None)
    if form.is_valid():
        teacher = form.save(commit=False)
        teacher.user = request.user
        teacher.save()
        return redirect('pages:studentaffair')
    context = {
         'form': form,
     }
    return render(request, 'teacher_create.html', context)