from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Courses, Lessons


class User(AbstractUser):
    """Класс для создания модели пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='почта пользователя')
    phone = models.CharField(max_length=35, verbose_name='телефон', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='город')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', blank=True, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payments(models.Model):
    """Класс для создания модели платежей"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'наличные'),
        ('card', 'безнал')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    date_pay = models.DateTimeField(auto_now=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='оплаченный курс')
    paid_lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='отдельно оплаченный урок')
    payment_sum = models.PositiveIntegerField(verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=150, choices=PAYMENT_METHOD_CHOICES, verbose_name='метод оплаты')
    payment_link = models.URLField(max_length=400, verbose_name='ссылка на оплату', blank=True, null=True)
    payment_id = models.CharField(max_length=255, verbose_name='идентификатор платежа', blank=True, null=True)

    def __str__(self):
        return f'{self.user}: {self.date_pay}, {self.payment_sum}, {self.payment_id}' \
               f'{self.paid_course if self.paid_course else self.paid_lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-date_pay']


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True, verbose_name='курс')

    def __str__(self):
        return f'{self.user}: {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'