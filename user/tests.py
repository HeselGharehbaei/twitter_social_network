from django.test import TestCase
from .models import Account, Follow


class AccountModelTestCase(TestCase):
    def setUp(self):
        self.user1 = Account.objects.create(
            username='user1', email='user1@example.com', 
            phone_number='09118778859')
        self.user2 = Account.objects.create(
            username='user2', email='user2@example.com', phone_number='09118778860')
        self.user3 = Account.objects.create(
            username='user3', email='user3@example.com', phone_number='09118778861')
        Follow.objects.create(from_user=self.user1, to_user=self.user2)
        Follow.objects.create(from_user=self.user2, to_user=self.user1)
        Follow.objects.create(from_user=self.user1, to_user=self.user3)

    def test_get_followers_and_following(self):
        following_count, following, followers_count, followers = self.user1.get_followers_and_following()
        self.assertEqual(following_count, 2)
        self.assertEqual(followers_count, 1)
        self.assertCountEqual(following, [('user2'), ('user3')])
        self.assertCountEqual(followers, [('user2')])      