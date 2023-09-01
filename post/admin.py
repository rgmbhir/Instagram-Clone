from django.contrib import admin
from .models import Tag, Post, Follow, Stream

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'picture', 'caption', 'posted', 'user', 'likes')

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Follow)
admin.site.register(Stream)