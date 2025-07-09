from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField('Phone Number',max_length=10,null=True,blank=True, help_text="max length is 10")
    joined_date = models.DateField('Joined Date',auto_now_add=True)
    profile_img = models.ImageField(upload_to='profile_picture',null = True , blank=True)
    terms_condition = models.BooleanField(default = False)
    def __str__(self) -> str:return self.user.get_full_name() or self.user.username

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField('Phone Number', max_length=10, help_text="max length is 10")
    location = models.CharField(max_length=100, blank=True, null=True)
    present_company = models.CharField(max_length=100, blank=True, null=True)
    resume = models.FileField(upload_to='instructor-reumes', blank=True, null=True)
    photo = models.ImageField(upload_to='intructor-photo', blank=True, null=True)
    joined_date = models.DateField('Joined Date',auto_now_add=True)

    def __str__(self) -> str:return self.user.get_full_name() or self.user.username

class SalesPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField('Phone Number',max_length=10, help_text="max length is 10")
    location = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='sales-person-photo', blank=True, null=True)

    def __str__(self) -> str:return self.user.get_full_name() or self.user.username

class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:return self.title


class NotificationStatus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null = True , blank = True)
    notice = models.ManyToManyField(Notice)
    def __str__(self) :
        return f"{self.student.user.username}"