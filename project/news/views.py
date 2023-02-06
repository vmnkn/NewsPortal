from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import get_object_or_404
from .tasks import notify_about_new_post_task
from django.core.cache import cache


class PostList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Post
    ordering = 'data'
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    paginate_by = 4
    permission_required = ('news.view_post',)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['time_now'] = datetime.utcnow()
        context['technical_work'] = None
        return context


class PostSearch(PostList):
    template_name = 'news/post_search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


class PostDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
    permission_required = ('news.view_post',)

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        if form.is_valid():
            notify_about_new_post_task.delay()
            return redirect('http://127.0.0.1:8000/news/')


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'
    permission_required = ('news.change_post',)


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)


class CategoryList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-data')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_sub'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'You are subscriber now.'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
