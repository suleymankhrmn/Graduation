from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save

from django.dispatch import receiver



# Create your models here.






class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=7, blank=True)
    age = models.CharField(max_length=3, blank=True)
    birth_date = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.user.username


   # def get_absolute_url(self):
    #    return reverse('post:detail', kwargs={'username': self.username})

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=3, blank=True)
    age = models.CharField(max_length=3, blank=True)

    def __str__(self):
        return self.user.username


class StudentAffairs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



    def __str__(self):
        return self.user.username



class Attendance(models.Model):
    student_id = models.CharField(max_length=20, null=True, blank=True)
    teacher_id = models.CharField(max_length=20, null=True, blank=True)
    lessons = models.CharField(max_length=15, null=True, blank=True)
    classroom = models.CharField(max_length=7, null=True, blank=True)
    attendance_date = models.DateField(null=True, blank=True)
    timing = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
         return self.classroom


class TimeTable(models.Model):
    classroom = models.CharField(max_length=7)
    dayname = models.CharField(max_length=20)
    lesson = models.CharField(max_length=20)
    l_time = models.CharField(max_length=202)



    def __str__(self):
        return '%s %s %s %s' % (self.classroom, self.dayname, self.time, self.lesson,)




class TeacherLesson(models.Model):
    classroom = models.CharField(max_length=7)
    lesson = models.CharField(max_length=20)
    teacher_id = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s' % (self.teacher_id, self.lesson)
