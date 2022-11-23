from news.models import Post
from news.views import PostDetail, PostUpdate, PostDelete


class ArticleDetail(PostDetail):
    queryset = Post.objects.filter(type='AR')


class ArticleUpdate(PostUpdate):
    queryset = Post.objects.filter(type='AR')


class ArticleDelete(PostDelete):
    queryset = Post.objects.filter(type='AR')
