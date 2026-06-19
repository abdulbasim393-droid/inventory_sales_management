from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create default user groups for role-based access control.'

    def handle(self, *args, **options):
        groups = ['Admin', 'Manager', 'Sales Staff']
        created = []

        for group_name in groups:
            group, created_flag = Group.objects.get_or_create(name=group_name)
            if created_flag:
                created.append(group_name)

        if created:
            self.stdout.write(self.style.SUCCESS(
                f'Created groups: {", '.join(created)}'
            ))
        else:
            self.stdout.write(self.style.NOTICE('All role groups already exist.'))
