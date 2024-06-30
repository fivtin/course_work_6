from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from mailer.forms import ClientForm, MessageForm, NewsletterUpdateForm, NewsletterCreateForm
from mailer.models import Client, Message, Newsletter


# Create your views here.


def index(request):
    return render(request, 'mailer/index.html')


class ClientListView(LoginRequiredMixin, ListView):
    login_url = "/users/login"

    model = Client

    def get_queryset(self):
        queryset = Client.objects.filter(owner=self.request.user)
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

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = VersionFormset(instance=self.object)
    #     return context_data
    #
    # def form_valid(self, form):
    #     formset = self.get_context_data()["formset"]
    #     self.object = form.save()
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #     return super().form_valid(form)

    # def get_form_class(self):
    #     user = self.request.user
    #     if user == self.object.user:
    #         return ProductForm
    #     elif user.has_perm('catalog.set_published') and \
    #             user.has_perm('catalog.set_category') and \
    #             user.has_perm('catalog.set_description'):
    #         return ProductModeratorForm
    #     else:
    #         raise PermissionDenied


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
        queryset = Message.objects.filter(owner=self.request.user)
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
        # for obj in context_data['object_list']:
        #     current_version = Version.objects.filter(product_id=obj.pk, is_current=True).first()
        #     obj.version = current_version
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

