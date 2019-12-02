import unittest

from app.model import Post,User,Comment
from app import db


class PostModelTest(unittest.TestCase):

    def setUp(self):
        self.new_post = Post(id=1,title='Test_post',subtitle='Test_subtitle', name='olga',content='Am testing a post')


    def test_check_instance_variables(self):
        self.assertEquals(self.new_post.title,'Test_post')
        self.assertEquals(self.new_post.content,'Am testing a post')

    def test_save_post(self):
        self.new_post.save_posts()
        self.assertTrue(len(Post.query.all())>0)

    def test_get_posts(self):
        self.new_post.save_posts()
        saved_post = Post.get_posts()
        self.assertTrue(saved_post is not None)

    def test_get_post_by_id(self):
        self.new_post.save_posts()
        post = Post.get_single_post(1)
        self.assertTrue(post is not None)
