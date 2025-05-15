from rest_framework import serializers
from .models import Course, Students


# самодельный сериализатор
class CourseSerializer_(serializers.Serializer):
    name = serializers.CharField(max_length=30)
    course_num = serializers.IntegerField()
    description = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()



# сериализатор основанный на модели
class CourseSerializer(serializers.ModelSerializer):
    # скрытоое поле будет в базу добавлять id пользователя который добавил запись
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ['id','name', 'course_num', 'description', 'user']



class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = '__all__'
        
  