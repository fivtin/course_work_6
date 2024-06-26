from django.urls import path
from django.views.decorators.cache import cache_page

from mailer.apps import MailerConfig
from mailer.views import index

# from catalog.views import ProductListView, ProductDetailView, ContactsTemplateView, ProductCreateView, \
#     ProductUpdateView, ProductDeleteView, CategoryListView

app_name = MailerConfig.name

urlpatterns = [
    path('', index),
    # path('', ProductListView.as_view(), name='product_list'),
    # path('category/', CategoryListView.as_view(), name='category_list'),
    # path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    # path('product/create', ProductCreateView.as_view(), name='product_create'),
    # path('product/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    # path('product/<int:pk>/delete', ProductDeleteView.as_view(), name='product_delete'),
    # path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
]
