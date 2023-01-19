from . import models
from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class APIModelsTests(APITestCase):

    def setUp(self) -> None:
        models.Mailing.objects.create(
            start=timezone.now(),
            finish=timezone.now() + timezone.timedelta(minutes=5),
            message='Test'
        )

        models.Client.objects.create(
            phone='79030001122'
        )

    def get_mailing_obj(self):
        return models.Mailing.objects.get(message='Test')

    def get_client_obj(self):
        return models.Client.objects.get(phone='79030001122')

    def test_get_mailings(self):
        obj = self.get_mailing_obj()
        query_obj = models.Mailing.objects.get_mailings().filter(message='Test')[0]
        self.assertEqual(obj, query_obj, 'объеткы не равны, метод get_mailings не работает')

    def test_urls_mailing(self):
        obj = self.get_mailing_obj()

        data = {
            'start': timezone.now(),
            'finish': timezone.now() + timezone.timedelta(minutes=5),
            'message': 'Test',
            'sending': True
        }

        response_get_all = self.client.get(reverse('mailing'))
        self.assertEqual(response_get_all.status_code, status.HTTP_200_OK)

        response_post = self.client.post(reverse('mailing'), data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        response_get = self.client.get(reverse('mailing_id', kwargs={'pk': obj.pk}))
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        response_put = self.client.put(reverse('mailing_id', kwargs={'pk': obj.pk}), data=data)
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_put.data), 7)

        response_get_mailing_messages = self.client.get(reverse('mailing_messages', kwargs={'mailing': obj.pk}))
        self.assertEqual(response_get_mailing_messages.status_code, status.HTTP_200_OK)

    def test_urls_client(self):
        obj = self.get_client_obj()

        data = {
            'phone': '9040001122',
            'utc': 'UTC+3'
        }

        response_get_all = self.client.get(reverse('client'))
        self.assertEqual(response_get_all.status_code, status.HTTP_200_OK)

        response_post = self.client.post(reverse('client'), data=data)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_post.data['code'], '904')
        self.assertEqual(response_post.data['teg'], 'UTC+3')

        response_get = self.client.get(reverse('client_id', kwargs={'pk': obj.pk}))
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        response_put = self.client.put(reverse('client_id', kwargs={'pk': obj.pk}), data={'phone': '9030001122'})
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        self.assertIn('7', response_put.data['phone'])


