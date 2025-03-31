from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
   path('admin/listings/comment/import-json/', views.import_json_comments, name='import_comments'),
   path('admin/listings/comment/export-json/', views.export_json_comments, name='export_comments'),
   path('admin/listings/comment/format/', views.format_comments, name='format_comments'),
   path('admin/listings/comment/data-clean/', views.clean_comments, name='clean_comments'),
] 