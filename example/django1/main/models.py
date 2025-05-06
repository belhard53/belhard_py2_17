from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Student(models.Model):
    name = models.CharField(
                max_length=30,
                verbose_name='Имя',
                null=False,
                blank=False)
                # unique = True
                #db_column #Имя столбца базы
                # db_comment
                # db_index 
                # editable        
                # error_messages # переопределить сообщения об ошибках - null, blank, invalid, unique_for_date
                # help_text #Дополнительный текст «помощи», который будет отображаться с виджетом формы.
                # unique_for_date
    
    surname = models.CharField(
                max_length=30,
                verbose_name='Фамилия')
    
    age = models.SmallIntegerField(
                null=True, 
                blank=True,
                validators=[MinValueValidator(18), MaxValueValidator(99)],
                verbose_name="Возраст")
    
    sex = models.CharField(
                max_length=10,
                choices=[('m', 'Мужчина'), ('f', 'Женщина')],
                verbose_name='Пол')
    
    active = models.BooleanField(verbose_name="Активный")
    
    # автоматическое поле  
    time_create = models.DateTimeField(
                null = True, 
                auto_now_add=True, 
                verbose_name="Время создания")
    # автоматическое поле 
    time_update = models.DateTimeField(
                null = True, 
                auto_now=True, 
                verbose_name="Время изменения")

    def __str__(self):
        return f"{self.name} {self.surname} ({self.age})"
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты" 
        indexes = [models.Index(fields=['surname'])]
        unique_together = [['name', 'surname']]
        # db_table = 'students'
        ordering = ["surname"]