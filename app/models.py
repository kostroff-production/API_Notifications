from django.db import models
from django.utils import timezone


class MailingManager(models.Manager):

    def get_mailings(self):
        return self.filter(start__lte=timezone.now(), finish__gte=timezone.now(), sending=False)


class Mailing(models.Model):

    CLIENT_TYPE_CHOOSE = (
        ('903', 'Beeline'),
        ('999', 'Yota'),
        ('925', 'Megafone'),
        ('915', 'MTC'),
        ('UTC+2', '#Калининград'),
        ('UTC+3', '#Москва'),
        ('UTC+4', '#Самара'),
        ('UTC+5', '#Екатеринбург'),
        ('UTC+6', '#Омск'),
        ('UTC+7', '#Красноярск'),
        ('UTC+8', '#Иркутск'),
        ('UTC+9', '#Якутск'),
        ('UTC+10', '#Владивосток'),
        ('UTC+11', '#Магадан'),
        ('UTC+12', '#Камчатка')
    )

    start = models.DateTimeField()
    finish = models.DateTimeField()
    message = models.TextField()
    type = models.CharField(
        max_length=6,
        choices=CLIENT_TYPE_CHOOSE,
        default='903'
    )
    sending = models.BooleanField(default=False)

    objects = MailingManager()

    class Meta:
        ordering = ['-start']

    def __str__(self):
        return str(self.pk)


class Client(models.Model):
    UTC_ZONE = (
        ('UTC+2', 'Калининград'),
        ('UTC+3', 'Москва'),
        ('UTC+4', 'Самара'),
        ('UTC+5', 'Екатеринбург'),
        ('UTC+6', 'Омск'),
        ('UTC+7', 'Красноярск'),
        ('UTC+8', 'Иркутск'),
        ('UTC+9', 'Якутск'),
        ('UTC+10', 'Владивосток'),
        ('UTC+11', 'Магадан'),
        ('UTC+12', 'Камчатка')
    )

    phone = models.CharField(max_length=11, unique=True)
    code = models.CharField(max_length=3, blank=True)
    teg = models.CharField(max_length=30, blank=True)
    utc = models.CharField(
        max_length=6,
        choices=UTC_ZONE,
        default='UTC+3'
    )
    start = models.TimeField(default='9:00:00')
    finish = models.TimeField(default='18:00:00')

    def __str__(self):
        return str(self.pk)


class Message(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)
    mailing = models.ForeignKey(Mailing, on_delete=models.SET_NULL, blank=True, null=True, related_name='mailing')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True, related_name='client')

    def __str__(self):
        return str(self.date)
