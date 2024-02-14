from django.contrib import admin

from users.models import Courses, Lessons


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    """Отображение списка курсов"""
    list_display = ('title', 'description')

@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    """Отображение списка уроков"""
    list_display = ('title', 'description', 'course')
