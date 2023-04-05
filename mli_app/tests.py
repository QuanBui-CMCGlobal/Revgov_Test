from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Patient, Group
from .serializers import PatientSerializer


class PatientTestCase(APITestCase):
    def setUp(self):
        self.group1 = Group.objects.create(name='Group 1')
        self.group2 = Group.objects.create(name='Group 2')
        self.patient1 = Patient.objects.create(name='John Doe', age=30, address='123 Main St')
        self.patient2 = Patient.objects.create(name='Jane Doe', age=25, address='456 Elm St', parent=self.patient1)

    def test_create_patient(self):
        url = reverse('patient-list')
        data = {
            'name': 'Bob Smith',
            'age': 40,
            'address': '789 Oak St',
            'groups': [{'name': 'Group 1'}, {'name': 'Group 2'}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 3)
        self.assertEqual(Patient.objects.last().name, 'Bob Smith')
        self.assertEqual(Patient.objects.last().groups.count(), 2)

    def test_add_patient_to_group(self):
        url = reverse('add-patient-to-group', kwargs={'pk': self.patient1.id})
        data = {'group_name': 'Group 2'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.patient1.groups.count(), 2)
        self.assertEqual(self.patient1.groups.last().name, 'Group 2')

    def test_search_patient(self):
        url = reverse('search-patient') + '?q=Jane'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PatientSerializer(instance=self.patient2)
        self.assertIn(serializer.data, response.data)