# django-easy-docs

A simple, opinionated way to add documentation to your website. Add a "Help" button to any page, and intuitively build the documentation for your Django app.

This project is still in its early stages of development, and any contributors are welcomed.

It has only been tested on Django 4.0 and up. For earlier Django releases, use with caution.

If you want to see something added, please request it! As I said, this is still in early development, and I am open to all suggestions. 

If you find a bug, please report it!

## Installation

This is an abridged installation. To properly install the app, please see the [documentation](https://lewisfletcher.github.io/django-easy-docs/installation.html).

Install via pip:

```bash
pip install django-easy-docs
```

You will need to add `easy_docs` to your `INSTALLED_APPS` in your `settings.py` file:

```python
INSTALLED_APPS = [
    ...
    'easy_docs',
    ...
]
```

You will also need to add the following to your `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('easy_docs/', include('easy_docs.urls')),
    ...
]
```

This package also takes advantage of several other packages, including:

- [django-markdownx](https://neutronx.github.io/django-markdownx/)
- [django-simple-history](https://django-simple-history.readthedocs.io/en/latest/)
- [django-htmx](https://django-htmx.readthedocs.io/en/latest/)
- [Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/) (required for modal functionality)

These are installed automatically when you install `django-easy-docs`, but you will need to add them to your `INSTALLED_APPS` as well:

```python
INSTALLED_APPS = [
    ...
    'markdownx',
    'simple_history',
    'django_htmx',
    ...
]
```

Please see each packages documentation for detailed installation/usage instructions. I also go over the basic installation of each in the Easy Docs [documentation](https://lewisfletcher.github.io/django-easy-docs/installation.html).

## Usage

To use Easy Docs, you will need to add the following to your base template:

```html
{% load easy_docs_tags %}

<head>
    ...
    {% load_dependencies %}
    ...
</head>

```

This will load the necessary dependencies for Easy Docs to work. You will then be able to load the help button on any page by adding the following to your template:

```html
{% load easy_docs_tags %}

<body>
    ...
    {% load_help_button %}
    ...
</body>
```

This will load the help button on any page that uses this template. If the page does not have any documentation and a staff member is logged in, it will open the documentation editor when clicked. If the page does have documentation, it will open the documentation viewer.

By default, the help button will be placed exactly where you place it in your template. The documentation editor supports Markdown, and will automatically render any Markdown in the documentation. For more information on Markdown, please see the [following guide](https://www.markdownguide.org/basic-syntax/).

To assist those who are not familiar with Markdown, the documentation editor also includes a live preview of the documentation. This preview will update as you type, and will show you exactly how the documentation will look when it is saved.

A backend system is also provided to allow you to manage the documentation for your site. You can access this by going to ``/docs/all-documentation/``, or by clicking the 'Documentation' header at the top of the document. You will need to be a staff member to access this page. It also includes version control with an option to easily revert to a previous documentation's save.

Documents are flaggable as public, which will allow them to be viewed by non-staff members. This is useful for adding documentation for your users.

For full usage instructions, please see the [documentation](https://lewisfletcher.github.io/django-easy-docs/usage.html).

## Documentation

For full documentation, please see the [documentation](https://lewisfletcher.github.io/django-easy-docs/).