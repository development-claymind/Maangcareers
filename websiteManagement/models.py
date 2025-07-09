from django.db import models

# Create your models here.
class Testimonial(models.Model):
    name = models.CharField(max_length=35)
    text = models.CharField(max_length=256)
    date = models.DateField()
    photo = models.ImageField(upload_to='testimonials')
    stars = models.CharField(max_length=2, choices=(
        ('0', '0 Stars'),
        ('1', '0.5 Stars'),
        ('2', '1 Star'),
        ('3', '1.5 Stars'),
        ('4', '2 Stars'),
        ('5', '2.5 Stars'),
        ('5', '2.5 Stars'),
        ('6', '3 Stars'),
        ('7', '3.5 Stars'),
        ('8', '4 Stars'),
        ('9', '4.5 Stars'),
        ('10', '5 Stars'),
    ))

    def __str__(self) -> str:return self.name

class Mentor(models.Model):
    name = models.CharField(max_length=35)
    subtext = models.CharField(max_length=50)
    maintext = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='mentors')

    def __str__(self) -> str:return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=100)
    answer = models.TextField()

    def __str__(self) -> str:return f"{self.question[:30]}..." if len(self.question) > 30 else self.question

class Blog(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    date = models.DateField()
    photo = models.ImageField(upload_to='blogs')
    popular = models.BooleanField(default=False)
    read_time = models.CharField(max_length=5, help_text='please input the number only; eg -> 5')
    views = models.BigIntegerField(default=0)

    @property
    def count_comments(self):return self.comment_set.count()

    def __str__(self) -> str:return f"{self.title[:30]}..." if len(self.title) > 30 else self.title

class BlogTopic(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self) -> str:return self.title

class Comment(models.Model):
    name = models.CharField(max_length=35)
    text = models.TextField()
    date = models.DateField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')

    def __str__(self) -> str:return f"{self.name[:30]}..." if len(self.name) > 30 else self.name