from django import forms

from blog.models import Blog


class BlogCreateForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ("title", "content", "preview", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'uk-checkbox'
            else:
                field.widget.attrs['class'] = 'uk-input'


class BlogUpdateForm(BlogCreateForm):

    class Meta:
        model = Blog
        fields = ("title", "content", "preview", )


class BlogManagerUpdateForm(BlogCreateForm):

    class Meta:
        model = Blog
        fields = ('is_published', )
