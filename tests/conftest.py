import pytest
from app import models
from django.utils import timezone
from django.contrib.auth.models import User


@pytest.fixture
def setUP(transactional_db):
    mailing = models.Mailing.objects.create(
        start=timezone.now(),
        finish=timezone.now() + timezone.timedelta(minutes=5),
        message='Test',
        type='999'
    )

    client = models.Client.objects.create(
        phone='79990001122',
        code='999',
        teg='UTC+3'
    )

    message = models.Message.objects.create(
        mailing=mailing,
        client=client
    )

    User.objects.create(
        username='admin',
        password='admin',
        email='root@yandex.ru'
    )
    return mailing, client, message



