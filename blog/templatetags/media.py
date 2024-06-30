from django import template

register = template.Library()


@register.simple_tag()
def url_media_tag(data):
    if data:
        return f'/media/{data}'
    return '#'


@register.filter()
def url_media_filter(data):
    if data:
        return f'/media/{data}'
    return '#'
