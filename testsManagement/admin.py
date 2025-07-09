from django.contrib import admin

# Register your models here.
from .models import *

class QuizAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'week',
        'course',
    )

    list_filter = (
        'course',
        'week',
    )

    search_fields = (
        'name',
    )
admin.site.register(Quiz, QuizAdmin)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'quiz',
        'course'
    )

    def course(self,obj) -> str:
        name = obj.quiz.course.name
        return name if len(name) < 30 else f"{name[:27]}..."

    list_filter = (
        'quiz',
        'quiz__course'
    )

    search_fields = (
        'question',
    )
admin.site.register(QuizQuestion, QuizQuestionAdmin)

class CompilerQuestionAdmin(admin.ModelAdmin):
    list_display = (
        'ques_title',
        'week',
        'day',
        'practice_or_mock',
        'disable',
    )

    list_filter = (
        'practice_mock',
        'week',
        'day',
        'disable',
        'google',
        'amazon',
        'microsoft',
        'meta',
        'linkedin',
        'uber',
        'adobe',
        'cred',
    )

    search_fields = (
        'ques_title',
        'prob_text',
    )
admin.site.register(CompilerQuestion, CompilerQuestionAdmin)
admin.site.register(QuizAttempt)
admin.site.register(QuestionTimer)
admin.site.register(CompilerQuestionLoadTemplate)
admin.site.register(CompilerQuestionAtempt)
admin.site.register(TaskSubmission)
admin.site.register(MessageDetails)
admin.site.register(SavePracticeCode)
admin.site.register(CourseSubmission)
admin.site.register(MockResult)