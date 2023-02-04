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
        
    def check_phone(self, phone):
        if len(phone) == 10:
            return '7' + phone
        return phone

    def create_code(self, phone):
        return re.search('9\d{0,2}', phone)[0]

    def to_internal_value(self, data):
        if len(data['phone']) < 10:
            raise ValueError('Phone number can`t be less than 10')
        return super().to_internal_value(data)

    def create(self, validated_data):
        validated_data['phone'] = self.check_phone(validated_data['phone'])
        validated_data['code'] = self.create_code(validated_data['phone'])
        validated_data['teg'] = validated_data['utc']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['phone'] = self.check_phone(validated_data['phone'])
        validated_data['code'] = self.create_code(validated_data['phone'])
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

