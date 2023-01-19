from django.urls import path
from . import views


urlpatterns = [
    path('client/', views.ClientListView.as_view(), name='client'),
    path('client/<int:pk>/', views.ClientView.as_view(), name='client_id'),
    path('mailing/', views.MailingStatisticAllView.as_view(), name='mailing'),
    path('mailing/<int:pk>/', views.MailingView.as_view(), name='mailing_id'),
    path('mailing/message/<int:mailing>/', views.MailingDetailView.as_view(), name='mailing_messages')
]
