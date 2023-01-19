import requests
import re
from requests.auth import AuthBase
from celery import shared_task
from . import models, serializers
from django.utils import timezone
from notifications.settings import config
from .exceptions import PostMessageException
from django.core.mail import send_mail
from django.contrib.auth.models import User
import logging
logger = logging.getLogger('tasks')


class TokenAuth(AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r


@shared_task(bind=True, autoretry_for=(PostMessageException, ), retry_kwargs={'max_retries': 3, 'countdown': 5})
def post_message(self, json):
    message = models.Message.objects.get(id=json['id'])

    with requests.post(
        url=config['foreign_api'] + json['id'],
        auth=TokenAuth(config['token']),
        json=json
    ) as response:
        logger.info(f'post_message(json): {json}')
        logger.info(f'post_message -> response.status_code {response.status_code}')
        logger.info(f'post_message -> response.text {response.text}')
        if response.status_code == 200:
            message.delivered = True
            message.save()
        else:
            logger.error(f'post_message -> Error send message {message.id} ')
            raise PostMessageException(f"Error send message {message.id}")


@shared_task
def send_message(id):
    mailing = models.Mailing.objects.get(id=id)

    try:
        int(mailing.type)
        clients = models.Client.objects.filter(code=mailing.type)
        hours = 0
    except ValueError:
        clients = models.Client.objects.filter(teg=mailing.type)
        hours = int(re.findall('UTC\\+(\d+)', mailing.type)[0]) - 3

    logger.info(f'send_message -> clients {clients}')

    while timezone.now() + timezone.timedelta(hours=hours) < mailing.finish:
        for client in clients:
            time_interval = timezone.now() + timezone.timedelta(hours=hours)
            if client.start < time_interval.time() < client.finish:
                message = models.Message.objects.create(
                    mailing=mailing,
                    client=client
                )
                json = {
                    "id": message.id,
                    "phone": client.phone,
                    "text": mailing.message
                }

                post_message.delay(json)
        break


@shared_task
def schedule_send():
    mailings = models.Mailing.objects.get_mailings()
    logger.info(f'schedule_send -> mailings {mailings}')

    for mailing in mailings:
        mailing.sending = True
        mailing.save()
        send_message.delay(mailing.id)


@shared_task
def send_statistic():
    user = User.objects.get(username='admin')
    logger.info(f'send_statistic -> user {user}, email {user.email}')
    mailings = models.Mailing.objects.all()
    serializer = serializers.MailingSerializer(mailings, many=True)
    mess = 'Отчет по всем рассылкам \n' + str(serializer.data)
    send_mail(
        subject='Статистика по рассылкам',
        message=mess,
        from_email=config['email']['address'],
        recipient_list=[user.email]
    )




