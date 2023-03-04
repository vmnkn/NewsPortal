from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('text', )
