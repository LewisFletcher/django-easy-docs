from django import forms
from .models import Documentation
from markdownx.fields import MarkdownxFormField

class DocumentationForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), help_text="The title of this documentation.")
    content = MarkdownxFormField()
    keywords = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), help_text="Comma separated list of keywords to help users find this documentation.", empty_value="Comma seperated list.")
    public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'large-checkbox'}), help_text="Check this box to make this documentation public.")
    reference_url = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())

    class Meta:
        model = Documentation
        fields = ('title', 'content', 'keywords', 'public', 'reference_url')

class ManualDocumentationForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), help_text="The title of this documentation.")
    content = MarkdownxFormField()
    keywords = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), help_text="Comma separated list of keywords to help users find this documentation.", empty_value="Comma seperated list.")
    public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'large-checkbox'}), help_text="Check this box to make this documentation public.")
    reference_url = forms.CharField(max_length=200, required=False, help_text="The URL of the page you are documenting, if any.", widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))

    class Meta:
        model = Documentation
        fields = ('title', 'content', 'keywords', 'public', 'reference_url')
