from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Note


class NotesAPITests(APITestCase):

    def setUp(self):
        self.note1 = Note.objects.create(body="First note")
        self.note2 = Note.objects.create(body="Second note")

    def test_get_all_notes(self):
        url = reverse('notes')
        response = self.client.get(url)

        print("Response data for get_all_notes:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_single_note(self):
        url = reverse('note', args=[self.note1.id])
        response = self.client.get(url)

        print("Single note response:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["body"], "First note")

    def test_create_note(self):
        url = reverse('create-note')
        data = {"body": "Created via test"}
        response = self.client.post(url, data)

        print("Create note response:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.count(), 3)

    def test_update_note(self):
        url = reverse('update-note', args=[self.note1.id])
        data = {"body": "Updated body"}
        response = self.client.put(url, data)

        print("Update response:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.body, "Updated body")

    def test_delete_note(self):
        url = reverse('delete-note', args=[self.note1.id])
        response = self.client.delete(url)

        print("Delete response:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Note.objects.count(), 1)
