from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Delete all posts from specified category'
    missing_args_message = 'Missing args'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'You really want to delete all posts from category {options["category"]}? (y/n)')
        if answer != 'y':
            self.stdout.write(self.style.ERROR('Access denied'))

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category == category).delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully delete all posts from category {category.name}'))

        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Category not find'))


