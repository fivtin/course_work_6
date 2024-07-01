from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from blog.models import Blog
from config.settings import CACHE_ENABLED
from mailer.forms import ClientForm, MessageForm, NewsletterUpdateForm, NewsletterCreateForm
from mailer.models import Client, Message, Newsletter, Attempt


# Create your views here.


def index(request):
    return render(request, 'mailer/index.html')


class ClientListView(LoginRequiredMixin, ListView):
    login_url = "/users/login"

    model = Client

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailer.access_manager'):
            queryset = Client.objects.all()
        else:
            queryset = Client.objects.filter(owner=user)
        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    login_url = "/users/login"

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')

    def form_valid(self, form):
        client = form.save()
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/users/login"

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailer:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/users/login"

    model = Client
    success_url = reverse_lazy('mailer:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    login_url = "/users/login"

    model = Message

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailer.access_manager'):
            queryset = Message.objects.all()
        else:
            queryset = Message.objects.filter(owner=user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    login_url = "/users/login"

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailer:message_list')

    def form_valid(self, form):
        message = form.save()
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/users/login"

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailer:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/users/login"

    model = Message
    success_url = reverse_lazy('mailer:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


class NewsletterDetailView(DetailView):

    model = Newsletter


class NewsletterListView(LoginRequiredMixin, ListView):
    login_url = "/users/login"

    model = Newsletter

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailer.set_block'):
            queryset = Newsletter.objects.all()
        else:
            queryset = Newsletter.objects.filter(owner=user)
        return queryset

    def get_template_names(self):
        user = self.request.user
        if user.has_perm('mailer.set_block'):
            return 'mailer/newsletter_manager_list.html'
        else:
            return 'mailer/newsletter_list.html'


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    login_url = "/users/login"

    model = Newsletter
    form_class = NewsletterCreateForm
    success_url = reverse_lazy('mailer:newsletter_list')

    def form_valid(self, form):
        newsletter = form.save()
        newsletter.owner = self.request.user
        newsletter.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['form'].fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return context_data


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/users/login"

    model = Newsletter
    form_class = NewsletterUpdateForm
    success_url = reverse_lazy('mailer:newsletter_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['form'].fields['clients'].queryset = Client.objects.filter(owner=self.request.user)
        return context_data


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/users/login"

    model = Newsletter
    success_url = reverse_lazy('mailer:newsletter_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner:
            return self.object
        raise PermissionDenied


def action_start(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.is_block = False
    newsletter.save()
    return redirect(reverse('mailer:newsletter_list'))


def action_stop(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.is_block = True
    newsletter.save()
    return redirect(reverse('mailer:newsletter_list'))


class IndexPageView(TemplateView):
    template_name = 'mailer/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if CACHE_ENABLED:
            context['all'] = cache.get('newsletters_all')
            if not context['all']:
                newsletters = Newsletter.objects.all()
                context['all'] = newsletters.count()
                cache.set('newsletters_all', context['all'])
                context['active'] = newsletters.filter(status=2).count()
                cache.set('newsletters_active', context['active'])
            else:
                context['active'] = cache.get('newsletters_active')

            context['clients'] = cache.get('clients_all')
            if not context['clients']:
                context['clients'] = Client.objects.count()
                cache.set('clients_all', context['clients'])
        else:
            newsletters = Newsletter.objects.all()
            context['all'] = newsletters.count()
            context['active'] = newsletters.filter(status=2).count()
            context['clients'] = Client.objects.count()

        blogs = Blog.objects.filter(is_published=True).order_by('?')[:3]
        context['object_list'] = blogs

        return context


class NewsletterStatisticList(TemplateView):
    template_name = 'mailer/newsletter_statistic.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletters = Newsletter.objects.filter(owner=self.request.user)
        for n in newsletters:
            attempts = Attempt.objects.filter(newsletter=n)
            n.success = attempts.filter(success=True).count()
            n.failure = attempts.filter(success=False).count()
        context['object_list'] = newsletters
        return context
