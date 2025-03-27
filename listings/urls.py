from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('import-json/', views.import_json, name='import_json'),
] 