import unittest
from user.models import Account
from .models import Post, Like

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, title='Test Post', text='This is a test post.')
        Like.objects.create(user=self.user, post=self.post, like=True)

    def tearDown(self):
        self.user.delete()
        self.post.delete()

    def test_is_liked_by_user(self):
        self.assertTrue(self.post.is_liked_by_user(self.user))

    def test_get_like_count(self):
        self.assertEqual(self.post.get_like_count(), 1)

    def test_get_comment_count(self):
        self.assertEqual(self.post.get_comment_count(), 0)

    def test_get_comments_and_users(self):
        comment = Comment.objects.create(text='This is a test comment.', user=self.user, post=self.post)
        comment_users, comment_count = self.post.get_comments_and_users()
        self.assertEqual(comment_count, 1)
        self.assertIn(self.user.username, comment_users)
        self.assertIn(comment.text, comment_users[self.user.username])

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