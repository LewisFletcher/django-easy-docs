from django import forms
from .models import Documentation
from markdownx.fields import MarkdownxFormField
from django.conf import settings

class BaseDocumentationForm(forms.ModelForm):
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), help_text="The title of this documentation.")
    content = MarkdownxFormField()
    keywords = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}), help_text="Comma separated list of keywords to help users find this documentation.", empty_value="Comma separated list.")
    public = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'large-checkbox'}), help_text="Check this box to make this documentation public.")
    regex_url = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        label='Regex Pattern'
    )
    
    class Meta:
        model = Documentation
        fields = ('title', 'content', 'keywords', 'public', 'regex_url')

    def __init__(self, *args, **kwargs):
        super(BaseDocumentationForm, self).__init__(*args, **kwargs)
        if not getattr(settings, 'USE_REGEX', False):
            self.fields['regex_url'].widget = forms.HiddenInput()
        else:
            self.fields['regex_url'].help_text += "Enter the regex pattern for this documentation. If the URL matches this pattern, this documentation will be shown."

class DocumentationForm(BaseDocumentationForm):
    reference_url = forms.CharField(
        max_length=200,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(settings, 'URL_MAP') and settings.URL_MAP:
            self.fields['reference_url'].widget = forms.TextInput(attrs={'class': 'form-control'})
            self.fields['reference_url'].help_text += "Enter the reference URL for this documentation. If it's mapped with the URL_MAP, make sure to match this with the mapped URL."
        else:
            self.fields['reference_url'].widget = forms.HiddenInput()

    class Meta(BaseDocumentationForm.Meta):
        fields = BaseDocumentationForm.Meta.fields + ('reference_url',)

class ManualDocumentationForm(BaseDocumentationForm):
    reference_url = forms.CharField(max_length=200, required=False, help_text="The URL of the page you are documenting, if any.", widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))

    class Meta(BaseDocumentationForm.Meta):
        fields = BaseDocumentationForm.Meta.fields + ('reference_url',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if hasattr(settings, 'URL_MAP') and settings.URL_MAP:
                self.fields['reference_url'].help_text += " If using URL_MAP, make sure to match this with the mapped URL."