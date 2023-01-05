from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed, post_save, post_init
from .models import PostCategory, Post
from project import settings


@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, **kwargs):
    html_content = render_to_string(
        'news/post_created_email.html',
        {
            'text': instance.text,
        }
    )

    message = EmailMultiAlternatives(
        subject=f'{instance.title}',
        body=f'{instance.text}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['valerijmanukyan.manukyan@yandex.ru'],
    )

    message.attach_alternative(html_content, 'text/html')

    message.send()

# def send_notifications(preview, pk, title, subscribers, ):
#     html_content = render_to_string(
#         'news/post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/news/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body=preview,
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers,
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# @receiver(m2m_changed, sender=PostCategory)
# def notify_about_new_post(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers: list[str] = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#         send_notifications(instance.preview(), instance.pk, instance.title, subscribers)
