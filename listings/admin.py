from django.contrib import admin
from listings.models import Comment  # Import the Comment model
from django.core.management import call_command
from django.contrib import messages
from django.urls import path
from django.shortcuts import render, redirect
import os

# Or, you can specify the fields to be displayed
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'body', 'postId', 'likes', 'user_id', 'username', 'full_name')
    actions = ['clean_data', 'format_data', 'export_data']
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-json/', self.import_json_view, name='import-json'),
            path('export-json/', self.export_json_view, name='export-json'),
            path('format-data/', self.format_data_view, name='format-data'),
            path('clean-data/', self.clean_data_view, name='clean-data'),
        ]
        return custom_urls + urls

    def import_json_view(self, request):
        if request.method == 'POST':
            try:
                file_path = request.POST.get('json_file')
                if file_path:
                    call_command('manage_listings', '--action', 'import', '--file', file_path)
                    self.message_user(request, f'Successfully imported data from {file_path}')
                else:
                    self.message_user(request, 'No file selected', level=messages.ERROR)
            except Exception as e:
                self.message_user(request, f'Error importing data: {str(e)}', level=messages.ERROR)
            return redirect('admin:listings_comment_changelist')
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_files = [f for f in os.listdir(project_root) if f.endswith('.json')]
        context = {
            'json_files': json_files,
            'opts': self.model._meta,
        }
        return render(request, 'admin/import_json.html', context)

    def export_json_view(self, request):
        if request.method == 'POST':
            try:
                file_name = request.POST.get('file_name', 'export.json')
                if not file_name.endswith('.json'):
                    file_name += '.json'
                
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                file_path = os.path.join(project_root, file_name)
                
                call_command('manage_listings', '--action', 'export', '--file', file_path)
                self.message_user(request, f'Successfully exported data to {file_name}')
            except Exception as e:
                self.message_user(request, f'Error exporting data: {str(e)}', level=messages.ERROR)
            return redirect('admin:listings_comment_changelist')
        
        context = {
            'opts': self.model._meta,
        }
        return render(request, 'admin/export_json.html', context)

    def format_data_view(self, request):
        if request.method == 'POST':
            try:
                call_command('manage_listings', '--action', 'clear')
                self.message_user(request, 'Successfully formatted data')
            except Exception as e:
                self.message_user(request, f'Error formatting data: {str(e)}', level=messages.ERROR)
            return redirect('admin:listings_comment_changelist')
        
        context = {
            'opts': self.model._meta,
        }
        return render(request, 'admin/format_data.html', context)
    
    def clean_data_view(self, request):
        if request.method == 'POST':
            try:
                call_command('manage_listings', '--action', 'data_clean')
                self.message_user(request, 'Successfully data cleaned')
            except Exception as e:
                self.message_user(request, f'Error cleaning data: {str(e)}', level=messages.ERROR)
            return redirect('admin:listings_comment_changelist')
        context = {
            'opts': self.model._meta,
        }
        return render(request, 'admin/clean_data.html', context)
# Register your models here.
# Register the Comment model with the custom admin interface
admin.site.register(Comment, CommentAdmin)

# Register your models here.
