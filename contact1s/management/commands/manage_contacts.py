from django.core.management.base import BaseCommand
from contact1s.models import Contact
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q

class Command(BaseCommand):
    help = 'Manage contact1s table: clear, import from JSON, export to JSON, or clean data'

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
            initial_count = Contact.objects.count()
            deleted_count = 0

            # Find and delete invalid entries
            invalid_entries = Contact.objects.filter(
                Q(id=0) |  # Invalid ID
                Q(email='') |  # Empty email
                Q(email__isnull=True) |  # Null email
                Q(email='anonymous') |  # Default email
                Q(full_name='') |  # Empty full name
                Q(full_name__isnull=True) |  # Null full name
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
                    f'Email: {entry.email}, '
                    f'Full Name: {entry.full_name}, '
                    f'Username: {entry.username}'
                ))

            # Delete invalid entries
            invalid_entries.delete()

            final_count = Contact.objects.count()
            self.stdout.write(self.style.SUCCESS(
                f'Data cleaning completed:\n'
                f'- Initial count: {initial_count}\n'
                f'- Deleted invalid entries: {deleted_count}\n'
                f'- Remaining entries: {final_count}'
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error cleaning data: {str(e)}'))

    def format_table(self):
        """Clear all contacts from the table"""
        try:
            Contact.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Successfully cleared contacts table'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error clearing table: {str(e)}'))

    def clean_contact_data(self, contact_data):
        """Clean and validate contact data"""
        cleaned_data = {
            'id': contact_data.get('id'),
            'username': contact_data.get('username', '').strip(),
            'full_name': contact_data.get('first_name', '').strip(),
            'email': contact_data.get('email', '').strip().lower()
        }
         # Validate and clean specific fields
        if not cleaned_data['id']:
            self.stdout.write(self.style.WARNING(f'Skipping contact with missing ID'))
            return None
        # Validate required fields
        if not cleaned_data['username'] or not cleaned_data['email']:
            return None
            
        return cleaned_data

    def import_from_json(self, file_path):
        """Import contacts from JSON file"""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
            if 'contacts' not in data:
                self.stdout.write(self.style.ERROR('Invalid JSON format: missing "contacts" key'))
                return
                
            initial_count = Contact.objects.count()
            imported_count = 0
            skipped_count = 0
            
            for contact_data in data['contacts']:
                cleaned_data = self.clean_contact_data(contact_data)
                if cleaned_data:
                    Contact.objects.create(**cleaned_data)
                    imported_count += 1
                else:
                    skipped_count += 1
                    
            final_count = Contact.objects.count()
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
        """Export contacts to JSON file"""
        try:
            contacts = Contact.objects.all()
            data = {'contacts': list(contacts.values())}
            
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2, cls=DjangoJSONEncoder)
                
            self.stdout.write(self.style.SUCCESS(f'Successfully exported {contacts.count()} contacts to {file_path}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error exporting data: {str(e)}'))
                    