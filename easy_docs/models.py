from django.db import models
from markdownx.models import MarkdownxField
from simple_history.models import HistoricalRecords
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.conf import settings
from .middleware import CurrentUserMiddleware
import re


class Documentation(models.Model):
    title = models.CharField(max_length=100, unique=True)
    title_slug = models.SlugField(max_length=100, unique=True)
    reference_url = models.CharField(max_length=200, unique=True, blank=True, null=True)
    regex_url = models.CharField(max_length=200, blank=True, null=True, help_text="Regular expression to match the URL of the page you are documenting, if any. Leave blank if this isn't needed.")
    content = MarkdownxField()
    keywords = models.TextField(null=False, blank=True, help_text="Comma separated list of keywords to help users find this documentation.")
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_documentations')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_documentations')
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.clean()
        current_user = CurrentUserMiddleware.get_current_user()
        if current_user and not current_user.is_anonymous:
            self.updated_by = current_user
            if not self.pk:
                self.created_by = current_user
        if not self.title_slug:
            self.title_slug = slugify(self.title)[:100]
        super(Documentation, self).save(*args, **kwargs)

    def clean(self):
        if self.reference_url:
            existing = Documentation.objects.filter(reference_url=self.reference_url).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError("A Documentation with this reference URL already exists.")
        if self.regex_url:
            existing = Documentation.objects.filter(regex_url=self.regex_url).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError("A Documentation with this regex URL already exists.")
            try:
                re.compile(self.regex_url)
            except re.error:
                raise ValidationError("Invalid regular expression.")
        super(Documentation, self).clean()

    def __str__(self):
        return self.title