from django.contrib import admin
from .models import *
from .helper import *
admin.site.register(Syllabus)

class BatchCompleteRequestAdmin(admin.ModelAdmin):
    list_display = ('batch', 'mentor', 'request_date', 'is_complete')
    list_filter = ('is_complete',)
    search_fields = ('batch__id', 'mentor__user__username')

    def get_queryset(self, request):
        return super().get_queryset(request).filter()

    def save_model(self, request, obj, form, change):
        if obj.is_complete == "aproved":
            batch_ = Batch.objects.filter(id=obj.batch.id)
            batch_.update(completed=True)
            student_list = list(batch_.values_list("students", flat=True))
            message = "Your course is completed"
            for i in student_list:
                email_id = Student.objects.filter(id=i).first().user.email
                email_send = sen_message(email_id, message)
                print(email_send)
        if obj.is_complete == "pending":
            batch_ = Batch.objects.filter(id=obj.batch.id).update(completed=False)
        if obj.is_complete == "not_aproved":
            batch_ = Batch.objects.filter(id=obj.batch.id).update(completed=False)
        super().save_model(request, obj, form, change)

admin.site.register(BatchCompleteRequest, BatchCompleteRequestAdmin)