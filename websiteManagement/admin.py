from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register((
    Testimonial,
    Mentor,
    FAQ,
))

class BlogTopicInline(admin.StackedInline):
    model = BlogTopic
    extra = 1
class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
class BlogAdmin(admin.ModelAdmin):
    inlines = (
        BlogTopicInline,
        CommentInline
    )

admin.site.register(Blog, BlogAdmin)