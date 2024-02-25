from django.contrib import admin
from .models import Post, Comment


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "slug", "updated"]
    search_fields = ['slug']
    prepopulated_fields = {'slug': ('body',)}
    list_filter = ['updated']
    raw_id_fields = ['user']


admin.site.register(Post, PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created", "is_reply"]
    raw_id_fields = ['user', 'post', 'reply']


