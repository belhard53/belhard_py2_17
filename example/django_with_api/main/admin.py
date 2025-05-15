from django.contrib import admin
from .models import Students, Course, Grade
# Register your models here.

admin.site.register(Course)
admin.site.register(Grade)

@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'surname', 'name','sex', 'active', 'average_grade1')
    search_fields = ('name', 'surname')
    list_filter = ('sex', 'active')
    prepopulated_fields = {"slug": ("name", "surname")}
    
    def short_name(self, obj):
        return f"{obj.surname} {obj.name[0]}."
    
    
    # вычисление среднего бала
    def average_grade1(self, obj):
        from django.db.models import Avg
        res = Grade.objects.filter(person=obj).aggregate(Avg('grade', default=0))
        return res['grade__avg']
    
    def average_grade2(self, obj):        
        gs = [g.grade for g in obj.grades.all()]
        return round(sum(gs)/len(gs),2) if gs else '---'
    
    short_name.short_description = 'Короткое имя'
    average_grade1.short_description = "Ср. бал"