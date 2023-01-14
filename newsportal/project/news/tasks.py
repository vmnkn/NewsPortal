from celery import shared_task
from .models import Category, Post, PostCategory
from .signals import send_notifications
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
import project.settings


@shared_task
def notify_about_new_post_task():
    print('Launch task: "notify_about_new_post_task"')
    pks = []
    queryset = Post.objects.all().order_by('pk').values('pk')
    for keys_dicts in queryset:
        for value in keys_dicts.values():
            pks.append(value)
    instance = Post.objects.get(pk=max(pks))
    categories = instance.category.all()
    subscribers: list[str] = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = [s.email for s in subscribers]

    send_notifications(instance.preview(), instance.pk, instance.title, subscribers)


@shared_task
def weekly_notify():
    print('Start task: "weekly_notify"')
    today = datetime.utcnow()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    if len(posts) == 0:
        pass
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'news/daily_post.html',
        {
            'link': project.settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Posts per week',
        body='',
        from_email=project.settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
