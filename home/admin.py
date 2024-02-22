from django.contrib import admin
from .models import Post
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "slug", "updated"]
    search_fields = ['slug']
    prepopulated_fields = {'slug': ('body',)}
    list_filter = ['updated']
    raw_id_fields = ['user']


admin.site.register(Post, PostAdmin)
