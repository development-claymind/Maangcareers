from django.db import models
from courseManagement.models import Course
from testsManagement.models import *
from userManagement.models import *
# Create your models here.



class Syllabus(models.Model):
    week = models.CharField(max_length=1,choices=(
        ('1', 'Week 1'),
        ('2', 'Week 2'),
        ('3', 'Week 3'),
        ('4', 'Week 4'),
        ('5', 'Week 5'),
        ('6', 'Week 6'),
        ('7', 'Week 7'),
        ('8', 'Week 8'),
    ))
    day = models.CharField(max_length=1, choices=(
        ('1','Day 1'),
        ('2','Day 2'),
        ('3','Day 3'),
    ))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True,blank=True)
    topic = models.CharField(max_length=128, null=True, blank=True)
    file = models.FileField(upload_to='upload_task')
    uploaded_at = models.DateTimeField(auto_now=True)                                             
    
    def __str__(self) :
        return f"Course -> {self.course.name}, Week-> {self.week}, Topic-> {self.topic}" 
    
class BatchCompleteRequest(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add = True)
    is_complete = models.CharField(max_length=30, choices=(
        ('pending','Pending'),
        ('aproved','Aproved'),
        ('not_aproved','Not Aproved'),
    ))

    objects = models.Manager()
    
    def __str__(self) :
        return f"Batch{self.batch.id} || {self.mentor.user.username} || {self.request_date.date()} || {self.is_complete}"