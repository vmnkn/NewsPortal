from django.urls import path
from news.views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('create/', PostCreate.as_view(), name='articles_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
]
