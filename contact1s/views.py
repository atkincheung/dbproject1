from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Contact

@staff_member_required
def import_json_contacts(request):
    try:
        # Your import logic here
        messages.success(request, 'Successfully imported contacts')
    except Exception as e:
        messages.error(request, f'Error importing contacts: {str(e)}')
    return redirect('admin:contact1s_contact_changelist')

@staff_member_required
def export_json_contacts(request):
    try:
        contacts = Contact.objects.all()
        data = {'contacts': list(contacts.values())}
        response = JsonResponse(data)
        response['Content-Disposition'] = 'attachment; filename="contacts.json"'
        return response
    except Exception as e:
        messages.error(request, f'Error exporting contacts: {str(e)}')
        return redirect('admin:contact1s_contact_changelist')

@staff_member_required
def format_contacts(request):
    try:
        # Your format logic here
        messages.success(request, 'Successfully formatted contacts')
    except Exception as e:
        messages.error(request, f'Error formatting contacts: {str(e)}')
    return redirect('admin:contact1s_contact_changelist')

@staff_member_required
def clean_contacts(request):
    try:
        # Your clean logic here
        messages.success(request, 'Successfully cleaned contacts')
    except Exception as e:
        messages.error(request, f'Error cleaning contacts: {str(e)}')
    return redirect('admin:contact1s_contact_changelist') # Create your views here.
