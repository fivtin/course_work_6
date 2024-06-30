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


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ("title", "start", "frequency", "message", "clients", )

        widgets = {
            'start': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # if not isinstance(field, forms.BooleanField):
            field.widget.attrs['class'] = 'uk-input'


class NewsletterUpdateForm(NewsletterForm):

    class Meta:
        model = Newsletter
        fields = ("title", "start", "frequency", "status",  "message", "clients", )

        widgets = {
            'start': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
