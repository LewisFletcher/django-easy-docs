from django.shortcuts import render
from .models import Documentation
from urllib.parse import unquote
from django.contrib.admin.views.decorators import staff_member_required
from .forms import DocumentationForm, ManualDocumentationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
import re

def get_document(request, page_url):
    decoded_url = unquote(page_url)
    if hasattr(settings, 'URL_MAP') and settings.URL_MAP:
        for pattern, replacement in settings.URL_MAP:
            try:
                if re.match(pattern, decoded_url):
                    decoded_url = re.sub(pattern, replacement, decoded_url)
                    break
            except re.error:
                print('Invalid regex pattern in URL_MAP: ', pattern)
                print(re.error)
                pass
    documentation = Documentation.objects.filter(reference_url=decoded_url)
    if documentation.exists():
        documentation = documentation.first()
        if documentation.public or request.user.is_staff:
            return render(request, 'doc_modal.html', {'documentation': documentation})
    use_regex = getattr(settings, 'USE_REGEX', False)
    if use_regex:
        for doc in Documentation.objects.filter(regex_url__isnull=False):
            try:
                regex_pattern = re.compile(doc.regex_url)
                if regex_pattern.match(decoded_url):
                    if doc.public or request.user.is_staff:
                        return render(request, 'doc_modal.html', {'documentation': doc})
            except re.error:
                print('Invalid regex pattern in Documentation: ', doc.regex_url)
                print(re.error)
                pass
    if request.user.is_staff:
        form = DocumentationForm()
        return render(request, 'create_documentation.html', {'url_ref': decoded_url, 'form': form})
    return render(request, 'not_found.html')

@staff_member_required
def create_documentation(request):
    if request.method == 'POST':
        form = DocumentationForm(request.POST, initial={'reference_url': request.POST.get('reference_url')})
        if form.is_valid():
            documentation = form.save()
            messages.success(request, 'Documentation created successfully!')
            return render(request, 'doc_modal.html', {'documentation': documentation})
        else:
            messages.error(request, 'There was an error creating the documentation:')
            messages.error(request, form.errors)
            return render(request, 'create_documentation.html', {'form': form})
    else:
        form = DocumentationForm(initial={'reference_url': request.GET.get('url_ref')})
        return render(request, 'create_documentation.html', {'form': form})
    
@staff_member_required
def edit_documentation(request, pk):
    documentation = get_object_or_404(Documentation, pk=pk)
    slug_view = request.GET.get('slug_view', False)
    context = {'documentation': documentation, 'slug_view': slug_view}
    if slug_view:
        template = 'edit_documentation_from_slug.html'
    else:
        template = 'edit_documentation.html'
    success_template = 'doc_modal.html'
    if request.method == 'POST':
        form = DocumentationForm(request.POST, instance=documentation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documentation updated successfully!')
            return render(request, success_template, context)
        else:
            context['form'] = form
            messages.error(request, 'There was an error updating the documentation:')
            messages.error(request, form.errors)
            return render(request, template, context)
    else:
        form = DocumentationForm(instance=documentation)
        context['form'] = form
        return render(request, template, context)
    
class AllDocumentation(ListView):
    model = Documentation
    template_name = 'all_documentation.html'
    context_object_name = 'documents'
    ordering = ['-updated_at']
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return 'documentation_list.html'
        return 'all_documentation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url"] = self.request.path
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(public=True)
        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            search_keywords = search_query.split(',')
            query = Q()
            for keyword in search_keywords:
                query |= Q(keywords__icontains=keyword.strip())
            queryset = queryset.filter(query)
        return queryset
    
def view_document(request, slug):
    documentation = get_object_or_404(Documentation, title_slug=slug)
    if documentation.public or request.user.is_staff:
        if request.htmx:
            return render(request, 'doc_modal.html', {'documentation': documentation})
        return render(request, 'view_documentation.html', {'documentation': documentation, 'slug_view' : True})
    else:
        raise Http404

@staff_member_required
def add_documentation(request):
    if request.method == 'POST':
        form = ManualDocumentationForm(request.POST)
        if form.is_valid():
            documentation = form.save()
            messages.success(request, 'Documentation created successfully!')
            return render(request, 'doc_modal.html', {'documentation': documentation})
        else:
            return render(request, 'create_documentation.html', {'form': form})
    else:
        form = ManualDocumentationForm()
        return render(request, 'create_documentation.html', {'form': form})


class HistoryView(DetailView):
    model = Documentation
    template_name = 'view_history.html'
    context_object_name = 'documentation'
    paginate_by = 10

    def get_template_names(self):
        if self.request.htmx:
            return 'history_list.html'
        return 'view_history.html'

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff:
            raise Http404
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url"] = self.request.path
        history_objects = context['documentation'].history.all().order_by('-history_date')
        paginator = Paginator(history_objects, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['history'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['page_obj'] = page_obj
        return context

@staff_member_required
def revert_history(request, pk, history_id):
    documentation = get_object_or_404(Documentation, pk=pk)
    history_record = documentation.history.get(pk=history_id)
    for field in history_record.instance._meta.fields:
        setattr(documentation, field.name, getattr(history_record, field.name))
    documentation.save()
    messages.success(request, 'Documentation reverted successfully!')
    return render(request, 'doc_modal.html', {'documentation': documentation})

@staff_member_required
def view_history_document(request, pk, history_id):
    documentation = get_object_or_404(Documentation, pk=pk)
    history = documentation.history.get(pk=history_id)
    return render(request, 'doc_modal.html', {'documentation': history.instance, 'history_view' : True, 'history_id' : history_id})