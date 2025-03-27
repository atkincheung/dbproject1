from django.core.management.base import BaseCommand
from listings.models import Comment
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

class Command(BaseCommand):
    help = 'Manage listings table: clear, import from JSON, export to JSON, or clean data'

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
            initial_count = Comment.objects.count()
            deleted_count = 0

            # Find and delete invalid entries
            invalid_entries = Comment.objects.filter(
                Q(id=0) |  # Invalid ID
                Q(user_id=0) |  # Invalid user ID
                Q(postId=0) |  # Invalid post ID
                Q(body='') |  # Empty body
                Q(body__isnull=True) |  # Null body
                Q(username='') |  # Empty username
                Q(username__isnull=True) |  # Null username
                Q(username='anonymous')  # Default username
            )

            # Count items to be deleted
            deleted_count = invalid_entries.count()

            # Log details of invalid entries before deletion
            self.stdout.write(self.style.WARNING(f'Found {deleted_count} invalid entries:'))
            for entry in invalid_entries:
                self.stdout.write(self.style.WARNING(
                    f'ID: {entry.id}, '
                    f'User ID: {entry.user_id}, '
                    f'Post ID: {entry.postId}, '
                    f'Username: {entry.username}, '
                    f'Body: {entry.body[:50]}...' if entry.body else 'Empty'
                ))

            # Delete invalid entries
            invalid_entries.delete()

            final_count = Comment.objects.count()
            self.stdout.write(self.style.SUCCESS(
                f'Data cleaning completed:\n'
                f'- Initial count: {initial_count}\n'
                f'- Deleted invalid entries: {deleted_count}\n'
                f'- Remaining entries: {final_count}'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cleaning data: {str(e)}'))

    def format_table(self):
        try:
            Comment.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared listings table'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing table: {str(e)}'))

    def clean_comment_data(self, comment_data):
        """Clean and validate comment data, providing default values for missing fields"""
        cleaned_data = {
            'id': comment_data.get('id'),
            'body': comment_data.get('body', 'No content provided'),
            'postId': comment_data.get('postId', 0),
            'likes': comment_data.get('likes', 0),
            'user_id': 0,
            'username': 'anonymous',
            'full_name': 'Anonymous User'
        }

        # Handle user data
        user_data = comment_data.get('user', {})
        if user_data:
            cleaned_data.update({
                'user_id': user_data.get('id', 0),
                'username': user_data.get('username', 'anonymous'),
                'full_name': user_data.get('fullName', 'Anonymous User')
            })

        # Validate and clean specific fields
        if not cleaned_data['id']:
            self.stdout.write(self.style.WARNING(f'Skipping comment with missing ID'))
            return None

        # Clean body text
        if cleaned_data['body']:
            cleaned_data['body'] = cleaned_data['body'].strip()

        # Ensure numeric fields are valid
        try:
            cleaned_data['postId'] = int(cleaned_data['postId'])
        except (ValueError, TypeError):
            cleaned_data['postId'] = 0

        try:
            cleaned_data['likes'] = int(cleaned_data['likes'])
        except (ValueError, TypeError):
            cleaned_data['likes'] = 0

        try:
            cleaned_data['user_id'] = int(cleaned_data['user_id'])
        except (ValueError, TypeError):
            cleaned_data['user_id'] = 0

        return cleaned_data

    def import_from_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                comments_data = json.load(file)
                
                successful_imports = 0
                skipped_imports = 0
                error_imports = 0
                
                for comment in comments_data:
                    cleaned_data = self.clean_comment_data(comment)
                    
                    if cleaned_data is None:
                        skipped_imports += 1
                        continue
                        
                    try:
                        Comment.objects.create(**cleaned_data)
                        successful_imports += 1
                        print(f'Successfully imported comment {cleaned_data["id"]}')
                        print(f'Comment data: {cleaned_data}')
                       
                    except Exception as e:
                        error_imports += 1
                        self.stdout.write(self.style.ERROR(f'Error importing comment {comment.get("id", "unknown")}: {str(e)}'))
                
                self.stdout.write(self.style.SUCCESS(
                    f'Import completed:\n'
                    f'- Successfully imported: {successful_imports}\n'
                    f'- Skipped: {skipped_imports}\n'
                    f'- Errors: {error_imports}'
                ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading JSON file: {str(e)}'))

    def export_to_json(self, file_path):
        try:
            comments = Comment.objects.all()
            comments_data = []
            
            for comment in comments:
                comment_dict = {
                    'id': comment.id,
                    'body': comment.body,
                    'postId': comment.postId,
                    'likes': comment.likes,
                    'user': {
                        'id': comment.user_id,
                        'username': comment.username,
                        'fullName': comment.full_name
                    }
                }
                comments_data.append(comment_dict)
            
            with open(file_path, 'w') as file:
                json.dump(comments_data, file, indent=2, cls=DjangoJSONEncoder)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully exported {len(comments_data)} comments to {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting comments: {str(e)}')) 