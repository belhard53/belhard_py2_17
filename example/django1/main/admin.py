from django.contrib import admin
from .models import Student, Course, Grade
# Register your models here.

admin.site.register(Grade)
admin.site.register(Course)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name', 'sex', 'average_grade')
    search_fields = ('name', 'surname')
    list_filter = ('sex', 'active')
    
    # для формирования slug
    prepopulated_fields = {"slug": ("name", "surname")}
    
    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."
    
    def average_grade(self, obj):
        gs = [g.grade for g in obj.grades.all()]
        return round(sum(gs)/len(gs),2) if gs else '---'
    
    
    def average_grade2(self, obj):
        from django.db.models import Avg
        res = Grade.objects.filter(person=obj).aggregate(Avg('grade', default=0))
        return res['grade__avg']
    
    short_name.short_description = "Короткое имя"
    