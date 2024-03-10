import datetime

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def users_deactivate():
    users = User.objects.all()
    time_old = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=30)
    for u in users:
        if u.last_login < time_old:
            u.is_active = False
            u.save()
