from django.test import TestCase
import unittest
from user.models import Account
from .models import Post, Like, Comment, Tag

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='testpass',
        email='user2@example.com', phone_number='09118778860')
        self.post = Post.objects.create(user=self.user, title='Test Post', text='This is a test post.')
        Like.objects.create(user=self.user, post=self.post, like=True)
        Comment.objects.create(user=self.user, post=self.post, text='Good luck')


    def tearDown(self):
        self.user.delete()
        self.post.delete()


    def test_get_like(self):
        likes, likes_count = self.post.get_like()
        likes = [(like.user) for like in likes]
        self.assertEqual(likes_count, 1)
        self.assertEqual(likes, [self.user])


    def test_get_comments(self):
        comments, comments_count = self.post.get_comments()
        comments = [(comment.user, comment.post) for comment in comments]
        self.assertEqual(comments_count, 1)
        self.assertEqual(comments, [(self.user, self.post)]) 


    def test_get_posts_by_tag(self):
        tag = Tag.objects.create(name='testtag')
        self.post.tags.add(tag)
        posts = Post.get_posts_by_tag('testtag')
        self.assertEqual(posts.count(), 1)
        self.assertIn(self.post, posts)
        

    def test_get_posts_by_user(self):
        posts = Post.get_posts_by_user(self.user)
        self.assertEqual(posts.count(), 1)
        self.assertIn(self.post, posts)