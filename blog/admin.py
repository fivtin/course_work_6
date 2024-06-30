from django.contrib import admin

from blog.models import Blog


# Register your models here.

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'preview', 'created_at', 'is_published', 'views_count', )
    list_filter = ('is_published',)
    search_fields = ('title', 'content', )
