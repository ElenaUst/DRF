from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from lms.models import Lessons, Courses
from users.models import User


class LessonsTestCase(APITestCase):
    """Тестирование CRUD для уроков"""

    def setUp(self) -> None:
        # super().setUp()
        self.client = APIClient()
        #Создание тестового пользователя
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )
        """Аутентификация тестового пользователя"""
        self.client.force_authenticate(user=self.user)

        #Создание тестового курса
        self.course = Courses.objects.create(
            title='test',
            owner=self.user

        )
        print(self.course)

        #Создание тестового урока

        # self.lesson = Lessons.objects.create(
        #     title='pagination',
        #     course=self.course,
        # )
        # print(self.lesson)

    def test_lessons_create(self):
        """Тестирование создания урока"""

        # Невалидные данные
        data = {
            'title': 'test create lesson',
            'link': 'yandex.ru',
            'course': self.course.pk
        }

        response = self.client.post('/lessons/create/', data=data)
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),

            {'link': ['Запрещено добавлять ссылки на сторонние ресурсы, кроме YouTube']}
        )
        self.assertFalse(
            Lessons.objects.all().exists()
        )
        #Валидные данные
        data = {
            'title': 'test create lesson',
            'course': self.course.pk,
            'link': 'https://www.youtube.com/watch?v=3g-j-fHUgJ4'
        }

        response = self.client.post('/lessons/create/', data=data)
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),

            {'id': 1,
             'title': 'test create lesson',
             'description': None,
             'preview': None,
             'link': 'https://www.youtube.com/watch?v=3g-j-fHUgJ4',
             'course': self.course.pk,
             'owner': self.user.pk}
        )
        self.assertTrue(
            Lessons.objects.all().exists()
    )

    def test_lessons_list(self):
        """Тестирование получения списка уроков"""
        # Создание тестового урока

        lesson = Lessons.objects.create(
            title='pagination',
            course=self.course,
            owner=self.user
        )
        print(lesson)

        response = self.client.get('/lessons/')
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
                {"count": 1,
                 "next": None,
                 "previous": None,
                 "results": [
        {
            "id": lesson.pk,
            "description": lesson.description,
            "title": lesson.title,
            "preview": None,
            "link": None,
            "course": lesson.course_id,
            "owner": lesson.owner_id}
            ]
                 }
        )

    def test_lessons_retrieve(self):
        """Тестирование получения одного урока"""
        # Создание тестового урока

        lesson = Lessons.objects.create(
            title='pagination',
            course=self.course,
            owner=self.user
        )
        print(lesson)

        response = self.client.get(reverse('lms:lessons_detail', args=[lesson.pk]))
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),

            {        "id": lesson.pk,
                     "description": lesson.description,
                     "title": lesson.title,
                     "preview": None,
                     "link": None,
                     "course": lesson.course_id,
                     "owner": lesson.owner_id}

        )


    def test_lessons_update(self):
        """Тестирование изменения урока"""
        # Создание тестового урока

        lesson = Lessons.objects.create(
            title='pagination',
            course=self.course,
            owner=self.user
        )
        print(lesson)
        data = {'title': 'validation'}
        response = self.client.patch(reverse('lms:lessons_update', args=[lesson.pk]), data=data)
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),

            {        "id": lesson.pk,
                     "description": lesson.description,
                     "title": 'validation',
                     "preview": None,
                     "link": None,
                     "course": lesson.course_id,
                     "owner": lesson.owner_id}

        )

    def test_lessons_delete(self):
        """Тестирование удаления урока"""
        # Создание тестового урока

        lesson = Lessons.objects.create(
            title='pagination',
            course=self.course,
            owner=self.user
        )
        print(lesson)

        response = self.client.delete(reverse('lms:lessons_delete', args=[lesson.pk]))

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(Lessons.objects.all().exists())




