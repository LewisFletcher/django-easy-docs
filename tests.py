from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseForbidden

from .models import Documentation

class StaffProtectedViewsTest(TestCase):
    def setUp(self):
        # Create a staff user
        self.staff_user = User.objects.create_user(username='staff_user', password='password')
        self.staff_user.is_staff = True
        self.staff_user.save()

        # Create a non-staff user
        self.non_staff_user = User.objects.create_user(username='non_staff_user', password='password')

        # Create a public document
        self.public_document = Documentation.objects.create(title='Public Document', content='This is a public document', public=True, reference_url='/test/')

        # Create a non-public document
        self.non_public_document = Documentation.objects.create(title='Non-Public Document', content='This is a non-public document', public=False, reference_url='/test2/')

    def test_public_document_accessible_by_staff(self):
        self.client.login(username='staff_user', password='password')
        response = self.client.get(reverse('get_document', args=[self.public_document.reference_url]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('documentation', args=[self.public_document.title_slug]))
        self.assertEqual(response.status_code, 200)

    def test_public_document_accessible_by_non_staff(self):
        self.client.login(username='non_staff_user', password='password')
        response = self.client.get(reverse('get_document', args=[self.public_document.reference_url]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('documentation', args=[self.public_document.title_slug]))
        self.assertEqual(response.status_code, 200)

    def test_non_public_document_accessible_by_staff(self):
        self.client.login(username='staff_user', password='password')
        response = self.client.get(reverse('get_document', args=[self.non_public_document.reference_url]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('documentation', args=[self.non_public_document.title_slug]))
        self.assertEqual(response.status_code, 200)

    def test_non_public_document_not_accessible_by_non_staff(self):
        self.client.login(username='non_staff_user', password='password')
        response = self.client.get(reverse('get_document', args=[self.non_public_document.reference_url]))
        self.assertContains(response, "Sorry, the document you requested does not exist.", status_code=200) # 200 because it's a custom error page
        response = self.client.get(reverse('documentation', args=[self.non_public_document.title_slug]))
        self.assertEqual(response.status_code, 404)

    def test_non_staff_cannot_edit_document(self):
        self.client.login(username='non_staff_user', password='password')
        response = self.client.get(reverse('edit_document', args=[self.public_document.pk]))
        self.assertEqual(response.status_code, 302) #redirects to login page

    def test_staff_can_edit_document(self):
        self.client.login(username='staff_user', password='password')
        response = self.client.get(reverse('edit_document', args=[self.public_document.pk]))
        self.assertEqual(response.status_code, 200)

    def test_non_staff_cannot_edit_private_document(self):
        self.client.login(username='non_staff_user', password='password')
        response = self.client.get(reverse('edit_document', args=[self.non_public_document.pk]))
        self.assertEqual(response.status_code, 302) #redirects to login page)

    def test_staff_can_edit_private_document(self):
        self.client.login(username='staff_user', password='password')
        response = self.client.get(reverse('edit_document', args=[self.non_public_document.pk]))
        self.assertEqual(response.status_code, 200)

    def test_non_staff_cannot_edit_document_from_slug(self):
        self.client.login(username='non_staff_user', password='password')
        response = self.client.get(reverse('edit_document', args=[self.public_document.pk]) + '?slug_view=true')
        self.assertEqual(response.status_code, 302) #redirects to login page

    def test_non_staff_cannot_view_document_history(self):
        self.client.login(username='non_staff_user', password='password')
        response = self.client.get(reverse('view_history', args=[self.public_document.pk]))
        self.assertEqual(response.status_code, 404)

    def test_non_staff_cannot_revert_document(self):
        self.client.login(username='non_staff_user', password='password')
        self.public_document.content = 'New content'
        self.public_document.save()
        history = self.public_document.history.first()
        response = self.client.get(reverse('revert_history', args=[self.public_document.pk, history.pk]))
        self.assertEqual(response.status_code, 302) #redirects to login page

    def test_non_staff_cannot_view_document_from_history(self):
        self.client.login(username='non_staff_user', password='password')
        self.public_document.content = 'New content'
        self.public_document.save()
        history = self.public_document.history.first()
        response = self.client.get(reverse('view_history_document', args=[self.public_document.pk, history.pk]))
        self.assertEqual(response.status_code, 302) #redirects to login page

    def test_staff_can_view_document_history(self):
        self.client.login(username='staff_user', password='password')
        response = self.client.get(reverse('view_history', args=[self.public_document.pk]))
        self.assertEqual(response.status_code, 200)

    def test_staff_can_revert_document(self):
        self.client.login(username='staff_user', password='password')
        self.public_document.content = 'New content'
        self.public_document.save()
        history = self.public_document.history.first()
        response = self.client.get(reverse('revert_history', args=[self.public_document.pk, history.pk]))
        self.assertEqual(response.status_code, 200)

    def test_staff_can_view_document_from_history(self):
        self.client.login(username='staff_user', password='password')
        self.public_document.content = 'New content'
        self.public_document.save()
        history = self.public_document.history.first()
        response = self.client.get(reverse('view_history_document', args=[self.public_document.pk, history.pk]))
        self.assertEqual(response.status_code, 200)

    def test_staff_can_view_document_from_slug(self):
        self.client.login(username='staff_user', password='password')
        response = self.client.get(reverse('edit_document', args=[self.public_document.pk]) + '?slug_view=true')
        self.assertEqual(response.status_code, 200)