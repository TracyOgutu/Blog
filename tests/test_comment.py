import unittest

from app.model import User,Comment,Post
from app import db


class CommentModelTest(unittest.TestCase):
    '''
    this is a test case for the class comments. for adding and saving new comments and to check if they are saved
    '''
    def setUp(self):
        self.new_post =Post(id=1,title='Test_post',content='Am testing a test post')

        self.new_comment = Comment(id=1,comment='Test comment',posts_id=self.new_post)

    def tearDown(self):
        Post.query.delete()
        User.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment,'Test comment')
        self.assertEquals(self.new_comment.posts_id,self.new_post)

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comments.query.all())>0)

    def test_get_comment(self):
        self.new_comment.save_comment()
        comment = Comments.get_comments(1)
        self.assertTrue(comment is not None)