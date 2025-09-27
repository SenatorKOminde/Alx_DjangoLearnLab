from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Set up user groups and permissions for the book management system'

    def handle(self, *args, **options):
        # Get the Book model content type
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get all book permissions
        can_view = Permission.objects.get(codename='can_view', content_type=book_content_type)
        can_create = Permission.objects.get(codename='can_create', content_type=book_content_type)
        can_edit = Permission.objects.get(codename='can_edit', content_type=book_content_type)
        can_delete = Permission.objects.get(codename='can_delete', content_type=book_content_type)
        
        # Create or get groups
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Viewers group'))
        else:
            self.stdout.write('Viewers group already exists')
        
        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Editors group'))
        else:
            self.stdout.write('Editors group already exists')
        
        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admins group'))
        else:
            self.stdout.write('Admins group already exists')
        
        # Assign permissions to Viewers group
        viewers_group.permissions.clear()
        viewers_group.permissions.add(can_view)
        self.stdout.write(self.style.SUCCESS('Assigned can_view permission to Viewers group'))
        
        # Assign permissions to Editors group
        editors_group.permissions.clear()
        editors_group.permissions.add(can_view, can_create, can_edit)
        self.stdout.write(self.style.SUCCESS('Assigned can_view, can_create, can_edit permissions to Editors group'))
        
        # Assign permissions to Admins group
        admins_group.permissions.clear()
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        self.stdout.write(self.style.SUCCESS('Assigned all permissions to Admins group'))
        
        self.stdout.write(
            self.style.SUCCESS(
                '\nGroups and permissions setup completed!\n'
                'Groups created:\n'
                '- Viewers: can_view\n'
                '- Editors: can_view, can_create, can_edit\n'
                '- Admins: can_view, can_create, can_edit, can_delete'
            )
        )