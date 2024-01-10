================
django-easy-docs
================

A simple, opinionated way to add documentation to your website. Add a "Help" button to any page, and intuitively build the documentation for your Django app.

This project is still in its early stages of development, and any contributors are welcomed.action-checkbox

It has only been tested on Django 4.0 and up. For earlier Django releases, use with caution.

If you want to see something added, please request it! As I said, this is still in early development, and I am open to suggestions. If you find a bug, please report it!


Installation
------------

Install via pip. ::

    pip install django-easy-docs

You will need to update your project's settings file to add ``easy_docs`` to your ``INSTALLED_APPS`` setting. ::

    INSTALLED_APPS = [
        ...
        "easy_docs",
        ...
    ]

You will also need to add the ``easy_docs`` URL to your project's ``urls.py`` file. ::

    from django.urls import path, include

    urlpatterns = [
        ...
        path("docs/", include("easy_docs.urls")),
        ...
    ]

This package also takes advantage of several other packages, including:

`Django Simple History <https://django-simple-history.readthedocs.io/en/latest/>`_
`Django MarkdownX <https://neutronx.github.io/django-markdownx/>`_
`Django HTMX <https://django-htmx.readthedocs.io/en/latest/>`_

These will come pre-installed with ``django-easy-docs``, but you will need to add them to your ``INSTALLED_APPS`` setting if you are not already using them. Please see their documentation for more information and follow their installation instructions.

For full installation instructions, please see the `documentation <https://django-easy-docs.readthedocs.io/en/latest/installation.html>`_.

Usage
-----

Easy docs is designed to be as simple as possible to use. Once installed, you can add a "Help" button to any page by adding the following to your template ::
    
    {% load easy_docs_tags %}
    {% help_button %}

This will add a blue button to the page that will open the documentation for that page. If the page does not have any documentation and a staff member is logged in, it will open the documentation editor.

The documentation supports Markdown, and will automatically render any Markdown in the documentation. For more information on Markdown, please see the documentation: https://www.markdownguide.org/basic-syntax/

A preview of the documentation will be shown in the editor while you write.

A backend system is also provided to allow you to manage the documentation for your site. You can access this by going to ``/docs/all-documentation/``, or by clicking the 'Documentation' header at the top of the document. You will need to be a staff member to access this page.

Documents are flaggable as public, which will allow them to be viewed by non-staff members. This is useful for adding documentation for your users.

For full usage instructions, please see the `documentation <https://django-easy-docs.readthedocs.io/en/latest/usage.html>`_.

Documentation
-------------

The documentation for this project is available `here <https://django-easy-docs.readthedocs.io/en/latest/>`_.

