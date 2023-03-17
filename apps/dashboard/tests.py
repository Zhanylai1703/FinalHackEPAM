from django.test import TestCase

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import date
from .models import Report
from apps.users.models import User


class ReportExportViewTestCase(APITestCase):
    

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password'
        )
        self.admin_group = Group.objects.create(name='admin')
        self.user.groups.add(self.admin_group)

    def test_export_report_admin_only(self):
        url = reverse('export-report')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(username='test_user', password='test_password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user.groups.add(self.admin_group)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/ms-excel')
        self.assertIn('attachment; filename="report.xls"', response['Content-Disposition'])
        # TODO: test that the file contains the expected data
