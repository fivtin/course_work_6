from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name


urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('create', BlogCreateView.as_view(), name='create'),
    path('<int:pk>', cache_page(60)(BlogDetailView.as_view()), name='detail'),
    path('<int:pk>/update', BlogUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', BlogDeleteView.as_view(), name='delete'),




]
