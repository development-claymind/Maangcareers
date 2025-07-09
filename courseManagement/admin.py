from django.contrib import admin
from .models import *
from django.urls import reverse
from mentorManagement.models import *

admin.site.site_header = "MAANGCareers Administration Page"
admin.site.index_title = "MAANGCareers Login"
admin.site.site_title = "MAANGCareers Admin"

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper

class lessonInline(admin.TabularInline):
    model = Topic
    extra = 0
class syllabusInline(admin.TabularInline):
    model = Week
    extra = 0
class batchInline(admin.StackedInline):
    model = Batch
    extra = 0
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "discount_percentage",
        "batch",
        "archive",
        "popular",
        "premium",
        "pre_recorded"
    )
    list_editable = list_display[4:]
    search_fields = list_display[:3]
    list_filter = list_display[4:]
    inlines = [
        # batchInline,
        syllabusInline,
        # lessonInline,
    ]
admin.site.register(Course,CourseAdmin)

class WeekAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "course",
    )
    search_fields = list_display
    list_filter = (
        'course',
    )
    inlines = [lessonInline]
admin.site.register(Week,WeekAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "week",
        "duration"
    )
    search_fields = list_display[:2]
    list_filter = (
        'week',
        'week__course'
    )
admin.site.register(Topic,TopicAdmin)

# class StudentInline(admin.TabularInline):
#     model = Student
#     extra = 0

class TimeTableInline(admin.TabularInline):
    model = TimeTable
    extra = 0
# class StudentInline(admin.TabularInline):
#     model = Batch.students.through
#     extra = 0
#     readonly_fields = (
#         'student',
#         'payment_id'
#     )

class StudentInline(admin.TabularInline):
    model = Batch.students.through
    extra = 0
    readonly_fields = (
        'student',
        'get_assign_project_topic',
        'payment_id'
    )
 
    def get_assign_project_topic(self, instance):
        a = str(instance.assign_topic)
        topic_name = "-"
        if a == None:
            pass
        else:
            info_parts = a.split(',')
            for part in info_parts:
                if "TopicName" in part:
                    topic_name = part.split(':')[1].strip()
                    break
        if instance.assign_project is None:
            assign_project = "NA"
            topic_name = ""
            return f"NA"
        else:
            assign_project = instance.assign_project
            return f"{assign_project}[{topic_name}]"
    get_assign_project_topic.short_description = 'Assign Project + Topic'  
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        exclude_fields = ['assign_topic', 'assign_project']
        for field_name in exclude_fields:
            if field_name in formset.form.base_fields:
                del formset.form.base_fields[field_name]
        return formset

#10/01/2024
class BatchAdmin(admin.ModelAdmin):
    change_form_template = "admin/custom_change_form.html" 
    list_display = (
        "name",
        "course",
        "enrolled",
        "instructor",
        "start_date",
        "end_date",
        "completed"
    )

    inlines = (TimeTableInline,StudentInline)

    # list_editable = list_display[2:-1]

    # filter_horizontal = ('students',)

    search_fields = ('name',)
    list_filter = (
        ('timetable__start_date', custom_titled_filter('TimeTable Start Date')),
        'course',
        'completed',
    )
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):  # for auto assign code 
        extra_context = extra_context or {}
        batch = Batch.objects.filter(id=object_id)
        try:
            batch_id = batch.first().id
        except:
            batch_id = 0
        extra_context['custom_button'] = True
        extra_context['batch_id'] = batch_id 
        url = reverse('stud-project-assign', args=[batch_id])
        context = {'custom_url': url}
        extra_context.update(context)
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    def save_model(self, request, obj, form, change):
        if obj.completed is True:
            req_batch = BatchCompleteRequest.objects.filter(batch_id=obj.id)
            if req_batch.exists():
                req_batch.update(is_complete="aproved")
            else:
                BatchCompleteRequest.objects.create(batch_id=obj.id, is_complete="aproved", mentor_id=obj.instructor.id)
        if obj.completed is False:
            req_batch = BatchCompleteRequest.objects.filter(batch_id=obj.id)
            if req_batch.exists():
                if req_batch.first().is_complete == "aproved":
                    req_batch.update(is_complete="pending")
        super().save_model(request, obj, form, change)
admin.site.register(Batch,BatchAdmin)

class TimeTableAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "start_time",
        "start_date",
        "start_time"
    )
    search_fields = list_display[1:]
    list_filter = (
        'start_date',
        'batch__course',
        'batch',
    )
admin.site.register(TimeTable,TimeTableAdmin)

class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "topic",
        "course",
        "week"
    )

    list_filter = (
        'course',
        'week'
    )

    search_fields = (
        'topic',
    )
admin.site.register(Note, NoteAdmin)
admin.site.register(ProjectName)
admin.site.register(ProjectTopic)
