from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users for different permission groups'

    def handle(self, *args, **options):
        # Get groups
        try:
            viewers_group = Group.objects.get(name='Viewers')
            editors_group = Group.objects.get(name='Editors')
            admins_group = Group.objects.get(name='Admins')
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Groups not found. Please run setup_groups command first.')
            )
            return

        # Create test users
        test_users = [
            {
                'username': 'viewer1',
                'email': 'viewer1@example.com',
                'password': 'testpass123',
                'date_of_birth': date(1990, 1, 1),
                'groups': [viewers_group]
            },
            {
                'username': 'editor1',
                'email': 'editor1@example.com',
                'password': 'testpass123',
                'date_of_birth': date(1985, 5, 15),
                'groups': [editors_group]
            },
            {
                'username': 'admin1',
                'email': 'admin1@example.com',
                'password': 'testpass123',
                'date_of_birth': date(1980, 10, 20),
                'groups': [admins_group]
            }
        ]

        for user_data in test_users:
            username = user_data['username']
            groups = user_data.pop('groups')
            
            # Create or get user
            user, created = User.objects.get_or_create(
                username=username,
                defaults=user_data
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {username}')
                )
            else:
                self.stdout.write(f'User {username} already exists')
            
            # Assign to groups
            user.groups.clear()
            for group in groups:
                user.groups.add(group)
            
            self.stdout.write(f'Assigned {username} to groups: {[g.name for g in groups]}')

        self.stdout.write(
            self.style.SUCCESS(
                '\nTest users created successfully!\n'
                'Login credentials:\n'
                '- viewer1 / testpass123 (Viewers group)\n'
                '- editor1 / testpass123 (Editors group)\n'
                '- admin1 / testpass123 (Admins group)'
            )
        )