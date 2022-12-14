from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter, ChoiceFilter
from .models import Author, Category, Post
from django import forms
from .resources import *


class PostFilter(FilterSet):
    search_title = CharFilter(
        field_name='title',
        label='Post title',
        lookup_expr='icontains',
    )

    search_author = ModelChoiceFilter(
        empty_label='All authors',
        field_name='author',
        label='Author',
        queryset=Author.objects.all(),
    )

    search_category = ModelChoiceFilter(
        empty_label='All categories',
        field_name='category',
        label='Category',
        queryset=Category.objects.all(),
    )

    post_date__gt = DateFilter(
        field_name='data',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date',
        lookup_expr='date__gte',
    )

    post_type = ChoiceFilter(choices=POST_TYPE)
    class Meta:
        model = Post
        fields = ['type']
