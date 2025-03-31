# from django.shortcuts import render
# from django.contrib import messages
# from django.shortcuts import redirect
# from django.contrib.admin.views.decorators import staff_member_required
# from django.http import JsonResponse
# from django.core.management import call_command
# from .models import Post
# import json
# import os

# # Create your views here.

# @staff_member_required
# def import_json_posts(request):
#     print(  "import_json_posts called with method:", request.method)
#     if request.method == 'POST':
#         print(  "import_json_posts called with method:POST", request.method)
#         try:
#             json_file = request.FILES.get('json_file')
#             if not json_file:
#                 messages.error(request, 'No file selected')
#                 return redirect('admin:posts_post_changelist')
                
#             data = json.loads(json_file.read().decode('utf-8'))
            
#             if 'posts' not in data:
#                 messages.error(request, 'Invalid JSON format: missing "posts" key')
#                 return redirect('admin:posts_post_changelist')
                
#             for post_data in data['posts']:
#                 Post.objects.create(
#                     title=post_data.get('title', ''),
#                     content=post_data.get('content', ''),
#                     author=post_data.get('author', '')
#                 )
                
#             messages.success(request, f'Successfully imported {len(data["posts"])} posts')
#         except json.JSONDecodeError:
#             messages.error(request, 'Invalid JSON file format')
#         except Exception as e:
#             messages.error(request, f'Error importing posts: {str(e)}')
#         return redirect('admin:posts_post_changelist')
    
#     return render(request, 'admin/posts/import_json.html')

# @staff_member_required
# def export_json_posts(request):
#     """
#     View to export all posts to a JSON file.

#     If the request method is GET, it exports all posts to a JSON file
#     and returns a JsonResponse with the file contents and
#     Content-Disposition header set to 'attachment; filename="posts_export.json"'.

#     If the request method is not GET, it renders a template to allow the user
#     to select a file name and submit the request.

#     :param request: the request object
#     :return: a JsonResponse with the file contents if the request method is GET,
#              or a rendered template if the request method is not GET
#     """
#     if request.method == 'POST':
#         try:
#             posts = Post.objects.all()
#             data = {'posts': list(posts.values())}
#             response = JsonResponse(data)
#             response['Content-Disposition'] = 'attachment; filename="posts_export.json"'
#             return response
#         except Exception as e:
#             messages.error(request, f'Error exporting posts: {str(e)}')
#     return render(request, 'admin/posts/post/export_json.html')

# @staff_member_required
# def format_posts(request):
#     if request.method == 'PoST':
#         try:
#             call_command('manage_posts', '--action=clear')
#             messages.success(request, 'Successfully formatted posts')
#         except Exception as e:
#             messages.error(request, f'Error formatting posts: {str(e)}')
#     return render(request, 'admin/posts/post/format_data.html')

# @staff_member_required
# def clean_posts(request):
#     """
#     View to clean all posts.

#     If the request method is POST, it runs the ``manage_posts`` management command
#     with the ``--action=data_clean`` option and redirects to the post changelist
#     page with a success message if the command is successful, or an error message
#     if it raises an exception.

#     If the request method is not POST, it renders a template to allow the user
#     to select the action and submit the request.

#     :param request: the request object
#     :return: a rendered template if the request method is not POST,
#              or a redirect to the post changelist page with a message if the
#              request method is POST
#     """
#     if request.method == 'POST':
#         try:
#             call_command('manage_posts', '--action=data_clean')
#             messages.success(request, 'Successfully cleaned posts')
#         except Exception as e:
#             messages.error(request, f'Error cleaning posts: {str(e)}')
#     return render(request, 'admin/posts/post/clean_data.html')
