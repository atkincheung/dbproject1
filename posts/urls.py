from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [

    # path('admin/posts/post/import-json/', views.import_json_posts, name='import_posts'),
    # path('admin/posts/post/export-json/', views.export_json_posts, name='export_posts'),
    # path('admin/posts/post/format/', views.format_posts, name='format_posts'),
    # path('admin/posts/post/clean/', views.clean_posts, name='clean_posts'),
     path('import-json/', views.import_json_posts, name='import_posts'),
     path('export-json/', views.export_json_posts, name='export_posts'),
     path('format-data/', views.format_posts, name='format_posts'),
     path('clean/', views.clean_posts, name='clean_posts'),
    
] 