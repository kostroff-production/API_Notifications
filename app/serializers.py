import re
from rest_framework import serializers
from .models import Mailing, Client, Message



class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('mailing', 'id', 'date', 'delivered', 'client')


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('phone', 'code', 'teg', 'utc', 'start', 'finish')

    def create(self, validated_data):
        validated_data['phone'] = '7' + validated_data['phone'] if len(validated_data['phone']) <= 10 else validated_data['phone']
        validated_data['code'] = re.search('7(\d{0,3})', validated_data['phone'])[1]
        validated_data['teg'] = validated_data['utc']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['phone'] = '7' + validated_data['phone'] if len(validated_data['phone']) <= 10 else validated_data['phone']
        return super().update(instance, validated_data)


class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        exclude = ('sending',)

    def validate(self, data):
        if data['start'] > data['finish']:
            raise ValueError('Дата начала не может быть позже даты окончания')
        return data

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'start': instance.start,
            'finish': instance.finish,
            'message': instance.message,
            'type': instance.type,
            'sending': instance.sending,
            'count_delivered': Message.objects.filter(mailing=instance.id, delivered=True).count(),
            'count_not_delivered': Message.objects.filter(mailing=instance.id, delivered=False).count(),
        }

