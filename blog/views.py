from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import BlogCreateForm, BlogUpdateForm, BlogManagerUpdateForm
from blog.models import Blog


# Create your views here.

class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = Blog.objects.all()
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    login_url = '/users/login'

    model = Blog
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.owner = self.request.user
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/users/login'

    model = Blog
    form_class = BlogUpdateForm

    def form_valid(self, form):
        if form.is_valid():
            blog = get_object_or_404(Blog, pk=self.kwargs.get('pk'))
            new_blog = form.save()
            if new_blog.is_published and blog.is_published != new_blog.is_published:
                new_blog.published_at = datetime.now()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return BlogUpdateForm
        elif user.has_perm('mailer.access_manager'):
            return BlogManagerUpdateForm
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/users/login'

    model = Blog
    success_url = reverse_lazy('blog:list')
