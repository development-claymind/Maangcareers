from django.db import models
from datetime import timedelta
from userManagement.models import Instructor, Student

class Course(models.Model):
    name = models.CharField(max_length=200)
    caption = models.CharField(max_length=100)
    price = models.IntegerField()
    discount_percentage = models.SmallIntegerField()

    @property
    def batch(self):return self.batches.filter(completed=False).count()

    archive = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)

    pre_recorded = models.BooleanField(default=False)

    lectures = models.SmallIntegerField()
    class_duration = models.CharField(max_length=5, help_text="please input here in format: hh:mm")
    course_duration = models.SmallIntegerField()
    projects = models.SmallIntegerField()
    mobile_computer = models.BooleanField(default=True)
    certificate = models.BooleanField(default=True)

    short_description = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()

    author_name = models.CharField(max_length=50)
    author_message = models.TextField(null=True, blank=True)
    author_photo = models.ImageField(upload_to="course_author_photos", default='default.png')

    thumbnail = models.FileField(upload_to="course_thumbnails")
    demo_video = models.URLField(null=True, blank=True)

    payment_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):return self.name

class Week(models.Model):
    name = models.CharField(max_length=50, help_text="Week number or Week Name")
    week = models.IntegerField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="syllabi")
    lock = models.BooleanField(default=False)

    def __str__(self):return self.name

class Topic(models.Model):
    name = models.CharField(max_length=64)
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="lessons")
    duration = models.DurationField(choices=(
        (timedelta(minutes=30),'30 min'),
        (timedelta(hours=1),'1 Hr'),
        (timedelta(hours=1, minutes=30),'1 Hr 30 min'),
        (timedelta(hours=2),'2 Hr'),
        (timedelta(hours=2, minutes=30),'2 Hr 30 min'),
        (timedelta(hours=3),'3 Hr'),
    ), null=True, blank=True)
    day = models.CharField(max_length=1, choices=(
        ("1", "Day 1"),
        ("2", "Day 2"),
        ("3", "Day 3"),),null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self) -> str:return self.name

class ProjectName(models.Model):
    project_name = models.TextField(null =True,blank=True)
    def __str__(self) -> str:return f"{self.project_name}"

class ProjectTopic(models.Model):
    project_topic = models.TextField(null =True,blank=True)
    project_name = models.ManyToManyField(ProjectName,help_text="After each eg press enter twice to create new project")
    def get_project_name(self):
        return [i["project_name"] for i in self.project_name.all().values("project_name")]
    def __str__(self) -> str:return f"TopicName : {self.project_topic}, ProjectName : {self.get_project_name()}"

class Batch(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="batches")
    project_topic = models.ForeignKey(ProjectTopic, on_delete=models.CASCADE , blank=True, null=True) #new add field
    max_participants = models.SmallIntegerField(default=30)

    start_date = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    completed = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True)

    instructor = models.ForeignKey(Instructor, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='batches')
    students = models.ManyToManyField(Student, related_name='batches', blank=True, through='BatchJoined')

    @property
    def enrolled(self) -> str:return f"{self.students.count()} / {self.max_participants}"

    @property
    # def name(self) -> str:return f"{self.course.name}_Batch_{self.pk}"
    def name(self) -> str:return f"Batch {self.pk} - {self.course.name}"

    def __str__(self) -> str:return self.name


    class Meta:verbose_name_plural = "batches"

    


# class BatchJoined(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="joined")
#     batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="joined")

#     payment_id = models.CharField(max_length=50, null=True, blank=True)
#     joined_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:return f"{self.student.__str__()} - {self.batch.name}"

class BatchJoined(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="joined")
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="joined")
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    assign_topic = models.ForeignKey(ProjectTopic, on_delete=models.CASCADE ,blank=True, null=True) #new add field
    assign_project = models.ForeignKey(ProjectName, on_delete=models.CASCADE,blank=True, null=True) #new add field
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:return f"{self.student.__str__()} - {self.batch.name}"

class TimeTable(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="timetable")

    topic = models.CharField(max_length=128, null=True, blank=True)

    start_time = models.TimeField()
    start_date = models.DateField()

    end_time = models.TimeField(null=True, blank=True)

    link = models.URLField(null=True, blank=True)
    week = models.CharField(max_length=1, choices=(
        ("1", "Week 1"),
        ("2", "Week 2"),
        ("3", "Week 3"),
        ("4", "Week 4"),
        ("5", "Week 5"),
        ("6", "Week 6"),
        ("7", "Week 7"),
        ("8", "Week 8"),
    ),null=True, blank=True)
    day = models.CharField(max_length=1, choices=(
        ("1", "Day 1"),
        ("2", "Day 2"),
        ("3", "Day 3"),),null=True, blank=True)
    def __str__(self) -> str:return f"{self.batch.name} - {self.start_date}"
        
class Note(models.Model):
    topic = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.CharField(max_length=1, choices=(
        ("1", "Week 1"),
        ("2", "Week 2"),
        ("3", "Week 3"),
        ("4", "Week 4"),
        ("5", "Week 5"),
        ("6", "Week 6"),
        ("7", "Week 7"),
        ("8", "Week 8"),
    ))
    file = models.FileField(upload_to="course_notes")

    def __str__(self) -> str:return f"{self.topic}"        
