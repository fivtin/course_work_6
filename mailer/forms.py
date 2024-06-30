from django import forms

from mailer.models import Client, Message, Newsletter


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ("email", "fio", "info", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # if not isinstance(field, forms.BooleanField):
            field.widget.attrs['class'] = 'uk-input'


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ("subject", "body", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # if not isinstance(field, forms.BooleanField):
            field.widget.attrs['class'] = 'uk-input'


class NewsletterCreateForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ("title", "start", "finish", "frequency", "message", "clients", )

        widgets = {
            'start': forms.TextInput(attrs={'type': 'datetime-local'}),
            'finish': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # if not isinstance(field, forms.BooleanField):
            field.widget.attrs['class'] = 'uk-input'

    def clean_finish(self):
        cleaned_data = self.cleaned_data.get('finish')
        if cleaned_data:
            start = self.cleaned_data.get('start')
            if start > cleaned_data:
                raise forms.ValidationError(f'Отказано. Дата окончания рассылки раньше даты её начала.')
        return cleaned_data


class NewsletterUpdateForm(NewsletterCreateForm):

    class Meta:
        model = Newsletter
        fields = ("title", "start", "finish", "frequency", "status",  "message", "clients", )

        widgets = {
            'start': forms.TextInput(attrs={'type': 'datetime-local'}),
            'finish': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
