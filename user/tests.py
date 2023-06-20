from django.test import TestCase
from .models import Account, Follow
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


class AccountModelTestCase(TestCase):
    def setUp(self):
        self.user1 = Account.objects.create(
            username='user1', email='user1@example.com')
        self.user2 = Account.objects.create(
            username='user2', email='user2@example.com')
        self.user3 = Account.objects.create(
            username='user3', email='user3@example.com')
        Follow.objects.create(from_user=self.user1, to_user=self.user2)
        Follow.objects.create(from_user=self.user2, to_user=self.user1)
        Follow.objects.create(from_user=self.user1, to_user=self.user3)

    def test_get_followers_and_following_count(self):
        following_count, following, followers_count, followers = self.user1.get_followers_and_following_count()
        self.assertEqual(following_count, 2)
        self.assertEqual(followers_count, 1)
        self.assertCountEqual(following, [('user2', None), ('user3', None)])
        self.assertCountEqual(followers, [('user2', None)])


CREATE_ACCOUNT_URL = reverse('account:create')
DELETE_ACCOUNT_URL = reverse('account:delete', args=[1])


class AccountTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = get_user_model().objects.create_user(
            email='testuser@test.com',
            password='testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_delete_account(self):
        """Test deleting an account"""

        # Create an account to delete
        payload = {
            'phone_number': '09123456789',
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpass',
            'first_name': 'Test',
            'last_name': 'User',
        }
        self.client.post(CREATE_ACCOUNT_URL, payload)

        # Delete the account
        response = self.client.delete(DELETE_ACCOUNT_URL)

        # Check that the account was deleted successfully
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(pk=1).exists())

    def test_delete_account_already_deleted(self):
        """Test deleting an account that has already been deleted"""

        # Create an account to delete
        payload = {
            'phone_number': '09123456789',
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password': 'testpass',
            'first_name': 'Test',
            'last_name': 'User',
            'deleted': True,
        }
        self.client.post(CREATE_ACCOUNT_URL, payload)

        # Try to delete the account
        response = self.client.delete(DELETE_ACCOUNT_URL)

        # Check that the account was not deleted
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Account.objects.filter(pk=1).exists())        