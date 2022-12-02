from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news/search/'


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news/search/')
