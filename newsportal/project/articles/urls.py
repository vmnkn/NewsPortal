from django.urls import path
from .views import ArticleDelete, ArticleUpdate, ArticleDetail
from news.views import PostCreate


urlpatterns = [
    path('<int:pk>', ArticleDetail.as_view(), name='post_detail'),
    path('<int:pk>/edit/', ArticleUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
    path('create/', PostCreate.as_view(), name='news_create'),
]
