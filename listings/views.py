from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Comment
import re
from django.db.models import Q

# Create your views here.

# @staff_member_required
# def import_json_comments(request):
#     try:
#         # Your import logic here
#         messages.success(request, 'Successfully imported comments')
#     except Exception as e:
#         messages.error(request, f'Error importing comments: {str(e)}')
#     return redirect('admin:listings_comment_changelist')

# @staff_member_required
# def export_json_comments(request):
#     try:
#         comments = Comment.objects.all()
#         data = {'comments': list(comments.values())}
#         response = JsonResponse(data)
#         response['Content-Disposition'] = 'attachment; filename="comments.json"'
#         return response
#     except Exception as e:
#         messages.error(request, f'Error exporting comments: {str(e)}')
#         return redirect('admin:listings_comment_changelist')

# @staff_member_required
# def format_comments(request):
#     try:
#         # Delete all comments
#         deleted_count = Comment.objects.all().delete()[0]
#         messages.success(request, f'Successfully deleted {deleted_count} comments')
#     except Exception as e:
#         messages.error(request, f'Error deleting comments: {str(e)}')
#     return redirect('admin:listings_comment_changelist')

# @staff_member_required
# def clean_comments(request):
#     try:
#         # Find comments where any of the specified fields are 0
#         comments_to_delete = Comment.objects.filter(
#             Q(user_id=0) |
#             Q(post_id=0) |
#             Q(username='0') |
#             Q(id=0) |
#             Q(body='0')
#         )
        
#         # Get the count before deletion
#         delete_count = comments_to_delete.count()
        
#         # Delete the filtered comments
#         comments_to_delete.delete()
        
#         if delete_count > 0:
#             messages.success(request, f'Successfully deleted {delete_count} comments with zero values')
#         else:
#             messages.info(request, 'No comments with zero values found')
            
#     except Exception as e:
#         messages.error(request, f'Error cleaning comments: {str(e)}')
    
#     return redirect('admin:listings_comment_changelist')
