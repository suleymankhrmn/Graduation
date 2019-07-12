from django.contrib import admin
from .models import Student
from .models import Teacher
from .models import StudentAffairs
from .models import Attendance
from .models import TimeTable
from .models import TeacherLesson

# Register your models here.

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentAffairs)
admin.site.register(Attendance)
admin.site.register(TimeTable)
admin.site.register(TeacherLesson)