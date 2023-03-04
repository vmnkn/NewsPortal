from django.contrib import admin
from .models import Post, Category
from modeltranslation.admin import TranslationAdmin


def restart_rating(modeladmin, request, queryset):
    queryset.update(post_rating=0)


restart_rating.short_description = 'Restart rating'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'data', 'rating', 'author')
    list_filter = ('post_rating', 'data')
    search_fields = ('title', 'category__name')
    actions = [restart_rating]


class TCategoryAdmin(TranslationAdmin):
    model = Category


class TPostAdmin(TCategoryAdmin):
    model = Post


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
