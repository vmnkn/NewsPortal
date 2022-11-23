from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Author
from django import forms


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

    post_date__gt = DateFilter(
        field_name='data',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Date',
        lookup_expr='date__gte',
    )
