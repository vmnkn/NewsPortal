from django.urls import path
from .views import ArticleDelete, ArticleUpdate, ArticleDetail


urlpatterns = [
    path('<int:pk>', ArticleDetail.as_view(), name='post_detail'),
    path('<int:pk>/edit/', ArticleUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
]
