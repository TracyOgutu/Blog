import unittest
from app.model import User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user=User(username = 'Kel',email = 'lop@gmail.com', password='banana')
        self.user_Trial = User(username = 'Kel',pass_secure = 'potato', email = 'lop@gmail.com')

    
    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('banana'))


    def test_save_user(self):
        self.new_user.save_user()
        self.assertTrue(len(User.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.user_Trial.username,'Kel')
        self.assertEquals(self.user_Trial.password,'banana')
        self.assertEquals(self.user_Trial.email,"lop@gmail.com")


    def tearDown(self):
        User.query.delete()