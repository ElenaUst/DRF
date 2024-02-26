from rest_framework.pagination import PageNumberPagination


class CoursesPagination(PageNumberPagination):
    """Класс для пагинации курсов"""
    page_size = 3  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр запроса для указания количества элементов на странице
    max_page_size = 10  # Максимальное количество элементов на странице


class LessonsPagination(PageNumberPagination):
    """Класс для пагинации уроков"""
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10
