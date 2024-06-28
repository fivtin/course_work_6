from django.urls import path
from django.views.decorators.cache import cache_page

from mailer.apps import MailerConfig
from mailer.views import index, ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = MailerConfig.name

urlpatterns = [
    path('', index),
    path('clients', ClientListView.as_view(), name='client_list'),
    path('clients/create', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update', ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete', ClientDeleteView.as_view(), name='client_delete'),
    path('messages', MessageListView.as_view(), name='message_list'),
    path('messages/create', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/update', MessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),
    # path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    # path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
]
