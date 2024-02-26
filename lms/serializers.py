from rest_framework import serializers

from lms.models import Courses, Lessons
from lms.validators import description_validator
from users.models import Subscription


class CoursesSerializer(serializers.ModelSerializer):
    """Класс сериализатора для курса"""
    lessons_count = serializers.SerializerMethodField()
    num_lessons = serializers.SerializerMethodField()
    subscribe = serializers.SerializerMethodField()


    def get_subscribe(self, course):
        """Метод для получения данных о наличии подписки на курс у пользователя"""
        user = self.context['request'].user
        for sub in Subscription.objects.filter(course=course):
            if sub.user == user:
                return f'Вы подписаны на обновления этого курса'

    def get_lessons_count(self, course):
        """Метод для вывода списка уроков, входящих в курс"""
        return [lesson.title for lesson in Lessons.objects.filter(course=course)]

    def get_num_lessons(self, course):
        """Метод для подсчета количества уроков, входящих в курс"""
        return Lessons.objects.filter(course=course).count()

    class Meta:
        model = Courses
        fields = '__all__'


class LessonsSerializer(serializers.ModelSerializer):
    """Класс сериализатора для урока"""
    link = serializers.CharField(validators=[description_validator], required=False)

    class Meta:
        model = Lessons
        fields = '__all__'


