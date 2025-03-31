from django.core.management.base import BaseCommand
from posts.models import Post
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

class Command(BaseCommand):
    help = 'Manage posts table: clear, import from JSON, export to JSON, or clean data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            help='Action to perform: clear, import, export, or data_clean',
            required=True
        )
        parser.add_argument(
            '--file',
            type=str,
            help='JSON file path for import/export',
            required=False
        )

    def handle(self, *args, **options):
        action = options['action']
        file_path = options.get('file')

        if action == 'clear':
            self.format_table()
        elif action == 'import':
            if not file_path:
                self.stdout.write(self.style.ERROR('Please provide a file path for import using --file'))
                return
            self.import_from_json(file_path)
        elif action == 'export':
            if not file_path:
                self.stdout.write(self.style.ERROR('Please provide a file path for export using --file'))
                return
            self.export_to_json(file_path)
        elif action == 'data_clean':
            self.data_clean()
        else:
            self.stdout.write(self.style.ERROR('Invalid action. Use: clear, import, export, or data_clean'))

    def data_clean(self):
        """Clean data by removing invalid entries"""
        try:
            initial_count = Post.objects.count()
            deleted_count = 0

            # Find and delete invalid entries
            invalid_entries = Post.objects.filter(
              #  Q(id=0) |  # Invalid ID
                Q(title='') |  # Empty title
                Q(title__isnull=True) |  # Null title
                Q(content='') |  # Empty content
                Q(content__isnull=True) |  # Null content
                Q(author='') |  # Empty author
                Q(author__isnull=True) |  # Null author
                Q(author='anonymous')  # Default author
            )

            # Count items to be deleted
            deleted_count = invalid_entries.count()

            # Log details of invalid entries before deletion
            self.stdout.write(self.style.WARNING(f'Found {deleted_count} invalid entries:'))
            for entry in invalid_entries:
                self.stdout.write(self.style.WARNING(
                    f'ID: {entry.id}, '
                    f'Title: {entry.title}, '
                    f'Author: {entry.author}'
                ))

            # Delete invalid entries
            invalid_entries.delete()

            final_count = Post.objects.count()
            self.stdout.write(self.style.SUCCESS(
                f'Data cleaning completed:\n'
                f'- Initial count: {initial_count}\n'
                f'- Deleted invalid entries: {deleted_count}\n'
                f'- Remaining entries: {final_count}'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cleaning data: {str(e)}'))

    def format_table(self):
        """Clear all posts from the table"""
        try:
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared posts table'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing table: {str(e)}'))

    def clean_post_data(self, post_data):
        """Clean and validate post data"""
        cleaned_data = {
            'title': post_data.get('title', '').strip(),
            'content': post_data.get('content', '').strip(),
            'author': post_data.get('author', '').strip()
        }
        
        # Validate required fields
        if not cleaned_data['title'] or not cleaned_data['content'] or not cleaned_data['author']:
            return None
            
        return cleaned_data

    def import_from_json(self, file_path):
        """Import posts from JSON file"""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
          #  if 'posts' not in data:
         #       self.stdout.write(self.style.ERROR('Invalid JSON format: missing "posts" key'))
          #      return
                
            initial_count = Post.objects.count()
            imported_count = 0
            skipped_count = 0
            
            for post_data in data['posts']:
                cleaned_data = self.clean_post_data(post_data)
                if cleaned_data:
                    Post.objects.create(**cleaned_data)
                    imported_count += 1
                else:
                    skipped_count += 1
                    
            final_count = Post.objects.count()
            self.stdout.write(self.style.SUCCESS(
                f'Import completed:\n'
                f'- Initial count: {initial_count}\n'
                f'- Imported: {imported_count}\n'
                f'- Skipped: {skipped_count}\n'
                f'- Final count: {final_count}'
            ))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON file'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))

    def export_to_json(self, file_path):
        """Export posts to JSON file"""
        try:
            posts = Post.objects.all()
            data = {'posts': list(posts.values())}
            
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2, cls=DjangoJSONEncoder)
                
            self.stdout.write(self.style.SUCCESS(f'Successfully exported {posts.count()} posts to {file_path}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting data: {str(e)}')) 