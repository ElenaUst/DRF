from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from lms.models import Lessons, Courses
from users.models import User


class LessonsTestCase(APITestCase):
    """Тестирование CRUD для уроков"""

    def setUp(self) -> None:
        self.client = APIClient()
        #Создание тестового пользователя
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )
        #Аутентификация тестового пользователя
        self.client.force_authenticate(user=self.user)

        #Создание тестового курса
        self.course = Courses.objects.create(
            title='test',
            owner=self.user

        )

    def test_lessons_create(self):
        """Тестирование создания урока"""

        # Невалидные данные
        data = {
            'title': 'test create lesson',
            'link': 'yandex.ru',
            'course': self.course.pk
        }

        response = self.client.post('/lessons/create/', data=data)

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        # Проверка вывода ошибки при вводе невалидных данных
        self.assertEqual(
            response.json(),

            {'link': ['Запрещено добавлять ссылки на сторонние ресурсы, кроме YouTube']}
        )
        # Проверка наличия записи в БД
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

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Проверка создания урока
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
        # Проверка наличия записи в БД
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

        response = self.client.get('/lessons/')

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Проверка вывода списка уроков
        self.assertEqual(
            response.json(),
            {"count": 1,
             "next": None,
             "previous": None,
             "results": [
                     {"id": lesson.pk,
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

        response = self.client.get(reverse('lms:lessons_detail', args=[lesson.pk]))

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Проверка вывода одного урока
        self.assertEqual(
            response.json(),

            {"id": lesson.pk,
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
        data = {'title': 'validation'}
        response = self.client.patch(reverse('lms:lessons_update', args=[lesson.pk]), data=data)

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Проверка обновления урока
        self.assertEqual(
            response.json(),

            {"id": lesson.pk,
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

        response = self.client.delete(reverse('lms:lessons_delete', args=[lesson.pk]))

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        # Проверка отсутствия удаленной записи в БД
        self.assertFalse(Lessons.objects.all().exists())


class CoursesTestCase(APITestCase):
    """Тестирование CRUD для курсов"""

    def setUp(self) -> None:
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )
        # Аутентификация тестового пользователя
        self.client.force_authenticate(user=self.user)

    def test_courses_create(self):
        """Тестирование создания курса"""
        data = {
            'title': 'test create course',
        }
        response = self.client.post(reverse('lms:courses-list'), data=data)
        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        # Проверка создания курса
        self.assertEqual(
            response.json(),

            {'id': 1,
             'lessons_count': [],
             'num_lessons': 0,
             'subscribe': None,
             'title': 'test create course',
             'preview': None,
             'description': None,
             'owner': self.user.pk}
        )
        # Проверка наличия записи в БД
        self.assertTrue(
            Courses.objects.all().exists()
        )

    def test_courses_list(self):
        """Тестирование получения списка курсов"""

        # Создание тестовых курсов
        course1 = Courses.objects.create(
            title='test_course1',
            owner=self.user,
        )
        course2 = Courses.objects.create(
            title='test_course2',
            owner=self.user,
        )

        response = self.client.get(reverse('lms:courses-list'))
        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Проверка вывода списка курсов
        self.assertEqual(
            response.json(),

            {'count': 2,
             'next': None,
             'previous': None,
             'results': [
                 {'id': course1.pk,
                  'lessons_count': [],
                  'num_lessons': 0,
                  'subscribe': None,
                  'title': course1.title,
                  'preview': None,
                  'description': None,
                  'owner': self.user.pk},
                 {'id': course2.pk,
                  'lessons_count': [],
                  'num_lessons': 0,
                  'subscribe': None,
                  'title': course2.title,
                  'preview': None,
                  'description': None,
                  'owner': self.user.pk},
             ]}
        )

    def test_courses_retrieve(self):
        """Тестирование получения одного курса"""

        # Создание тестового курса
        course = Courses.objects.create(
            title='test_course',
            owner=self.user
        )

        response = self.client.get(reverse('lms:courses-detail', args=[course.pk]))

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка вывода курса
        self.assertEqual(
            response.json(),

             {'id': course.pk,
              'lessons_count': [],
              'num_lessons': 0,
              'subscribe': None,
              'title': course.title,
              'preview': None,
              'description': course.description,
              'owner': self.user.pk},

        )

    def test_courses_update(self):
        """Тестирование изменения курса"""
        # Создание тестового курса

        course = Courses.objects.create(
            title='test_course',
            owner=self.user
        )
        data = {'title': 'test_course_change'}
        response = self.client.patch(reverse('lms:courses-detail', args=[course.pk]), data=data)
        print(response.json())

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Проверка обновления курса
        self.assertEqual(
            response.json(),

            {"id": course.pk,
             'lessons_count': [],
              'num_lessons': 0,
              'subscribe': None,
              'title': 'test_course_change',
              'preview': None,
              'description': course.description,
              'owner': self.user.pk},
        )

    def test_courses_delete(self):
        """Тестирование удаления курса"""
        # Создание тестового курса

        course = Courses.objects.create(
            title='test_course',
            owner=self.user
        )

        response = self.client.delete(reverse('lms:courses-detail', args=[course.pk]))

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        # Проверка отсутствия удаленной записи в БД
        self.assertFalse(Courses.objects.all().exists())

