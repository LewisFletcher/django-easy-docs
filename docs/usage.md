# Usage

## Add the Help Button
{% raw %}
If you want a page to have documentation associated with it, add `{% help_button %}` to the template wherever you would like the help button to be. Ensure you load the help tag by adding `{% load easy_docs_tags %}` to the top of the template, and that you have loaded the dependencies by adding `{% load_dependencies %}` to the `<head>` of your base template.
{% endraw %}
## Create docs
- A staff member, when clicking help, will open the documentation editor if there is no documentation associated with the page.
- The slugs and URL references are taken care of behind the scenes, based on the URL of the page the help button is on.
- Check the ‘public’ box to make the document available to non-staff members. This can be modified at any time (by staff members).
- Alternatively, inside of the 'all documents' (available at '/docs/all-documentation/) section, a document can be added manually by a staff member.

## View docs
- Once a doc has been created, it can be revealed by clicking the help button or by finding it in the ‘all documents’ section. The 'all documents' section also supports searching by keywords separated by commas.
- If a user is a staff member, they will see an option to edit the docs at the bottom of the documentation once it has been revealed.
- To view all documents, click the ‘Documentation’ header in the modal box. This is a protected and won’t show non-public documents to non-staff members.
- To view a specific document by slug in a seperate page (useful for sending or finding documents), click the document title.

## Edit docs
- If a user is a staff member, they will see an Edit link in the bottom left corner of the doc. This will bring the editor into the viewport.
- The editor supports Markdown, and will automatically render any Markdown in the documentation. For more information on Markdown, please see the [following guide](https://www.markdownguide.org/basic-syntax/).
- To assist those who are not familiar with Markdown, the documentation editor also includes a live preview of the documentation. This preview will update as you type, and will show you exactly how the documentation will look when it is saved.
- To save the document, click the Save button in the bottom right corner of the doc. This will save the document and bring you back to the document view.
- If a document was edited by mistake, the previous version can be restored by clicking the Revert Doc button after clicking the History link in the bottom right corner of the doc and finding the version you would like to revert to. (See below for more information on history)

## View history
- If a user is a staff member, they will see a History link in the bottom right corner of the doc. This will take them to the history view.
- All the history of the document is displayed here. Clicking on an instance will bring up that version in the viewport.
- To revert to the version being displayed, click Revert Doc in the bottom left corner.

## Delete docs
- Docs can currently only be deleted in the admin site. This is to prevent accidental deletion of docs.
- If this feature is requested, I will add it in a future release.
