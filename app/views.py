from rest_framework import generics
from . import serializers, models
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view


class ClientListView(generics.ListCreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


@extend_schema_view(patch=extend_schema(exclude=True))
class ClientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


@extend_schema_view(patch=extend_schema(exclude=True))
class MailingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Mailing.objects.all()
    serializer_class = serializers.MailingSerializer


class MailingStatisticAllView(generics.ListCreateAPIView):
    queryset = models.Mailing.objects.all()
    serializer_class = serializers.MailingSerializer


class MailingDetailView(generics.ListAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    lookup_field = 'mailing'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}

        filter_queryset = queryset.filter(**filter_kwargs)

        page = self.paginate_queryset(filter_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(filter_queryset, many=True)
        return Response(serializer.data)
