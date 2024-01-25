from django import template
from django.utils.safestring import mark_safe
from django.templatetags.static import static
import markdown as md
from django.template.loader import render_to_string

register = template.Library()

@register.simple_tag
def load_dependencies():
    css_url = static('easy_docs/css/styles.css')
    return mark_safe(f"""
    <!-- Include AlpineJS -->
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@2" defer></script>
    <!-- Include htmx -->
    <script src="https://unpkg.com/htmx.org/dist/htmx.js"></script>
    <!-- Include custom css -->
    <link href="{css_url}" rel="stylesheet">
    """
    )

@register.filter(name='markdown')
def markdown_format(text):
    return md.markdown(text, extensions=['markdown.extensions.fenced_code'])

@register.simple_tag(takes_context=True)
def help_button(context):
    context_dict = {k: v for k, v in context.flatten().items()}
    return render_to_string('documentation.html', context_dict)