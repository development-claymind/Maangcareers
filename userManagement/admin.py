from typing import Any, List, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import *
from testsManagement.models import Quiz
from django.contrib.admin import SimpleListFilter
from datetime import date

class EnrolledListFilter(SimpleListFilter):
    title = 'Currenty Enrolled'
    parameter_name = 'enroled'
    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return (
            ('true','Enrolled'),
            ('false','Not Enrolled')
        )
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'true':return queryset.filter(batches__end_date__gte = date.today())
        elif self.value() == 'false':return queryset.filter(batches__end_date__lt = date.today())
        return queryset

class BatchInline(admin.TabularInline):
    model = Student.batches.through
    extra = 0
class QuizAttempInline(admin.TabularInline):
    model = Quiz.students.through
    extra = 0
    exclude = ('answers',)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'phone_num',
        'user_email',
        'latest_batch',
        'joined_date',
    )
    def user_email(self, obj) -> str:return obj.user.email
    def latest_batch(self, obj) -> str: return obj.batches.last()
    inlines = (
        BatchInline,
        QuizAttempInline
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
    )
    list_filter = (
        'joined_date',
        EnrolledListFilter,
    )
admin.site.register(Student, StudentAdmin)

class InstructorAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'phone_num',
        'joined_date',
        'present_company'
    )
    search_fields = (
        'user__first_name',
        'user__last_name'
        'present_company'
    )
admin.site.register(Instructor, InstructorAdmin)

class salesPersonAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'phone_num',
    )
    search_fields = (
        'user__first_name',
        'user__last_name'
    )
admin.site.register(SalesPerson, salesPersonAdmin)

class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'date',
    )
    search_fields = (
        'title',
    )
admin.site.register(Notice, NoticeAdmin)
admin.site.register(NotificationStatus)