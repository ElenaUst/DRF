from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from lms.models import Courses
from users.models import Subscription


@shared_task
def send_mail_update_course(update_course_id):
    """Функция отправки уведомлений при обновлении курса"""
    course_id = Courses.objects.get(pk=update_course_id)
    print(course_id)
    # Получение подписчиков курса
    subscribers = Subscription.objects.filter(course=course_id)

    print(subscribers)
    if subscribers:
        for sub in subscribers:
            to_email = sub.user.email
            subject = 'Обновления материалов курса'
            message = 'Курс был обновлен'
            send_mail(
                subject=subject,
                message=message,
                recipient_list=[to_email],
                from_email=EMAIL_HOST_USER,
                fail_silently=True
            )


