from django.contrib import admin

from users.models import User, Payments


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение списка пользователей"""
    list_display = ('phone', 'email',)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    """Отображение списка платежей"""
    list_display = ('user', 'date_pay', 'paid_course','paid_lesson')

