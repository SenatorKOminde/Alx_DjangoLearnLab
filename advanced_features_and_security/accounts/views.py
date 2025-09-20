from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required, login_required
from .permissions_models import SecureDocument

@login_required
@permission_required('accounts.can_view', raise_exception=True)
def document_list(request):
    documents = SecureDocument.objects.filter(owner=request.user)
    return render(request, 'accounts/document_list.html', {'documents': documents})

@login_required
@permission_required('accounts.can_create', raise_exception=True)
def document_create(request):
    # Implementation for creating a document
    pass

@login_required
@permission_required('accounts.can_edit', raise_exception=True)
def document_edit(request, pk):
    # Implementation for editing a document
    pass

@login_required
@permission_required('accounts.can_delete', raise_exception=True)
def document_delete(request, pk):
    # Implementation for deleting a document
    pass
