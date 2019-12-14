from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            email='normal@example.org',
            first_name="Normal",
            last_name="User",
            password='foobar'
        )
        self.assertEqual(user.email, 'normal@example.org')
        self.assertEqual(user.first_name, 'Normal')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(ValueError):
            user_model.objects.create_user(
                email='',
                first_name='Normal',
                password="foobar"
            )
        with self.assertRaises(ValueError):
            user_model.objects.create_user(
                email='normal2@exmaple.org',
                first_name='',
                password='foobar'
            )
        with self.assertRaises(ValueError):
            user_model.objects.create_user(
                email='normal3@exmaple.org',
                first_name='Normal',
                password=''
            )

    def test_create_superuser(self):
        user_model = get_user_model()
        admin_user = user_model.objects.create_superuser(
            email='super@example.org',
            first_name="Super",
            last_name="user_model",
            password='foobar'
        )
        self.assertEqual(admin_user.email, 'super@example.org')
        self.assertEqual(admin_user.first_name, 'Super')
        self.assertEqual(admin_user.last_name, 'user_model')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        with self.assertRaises(TypeError):
            user_model.objects.create_superuser()
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email='',
                first_name='Super',
                password="foobar"
            )
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email='super2@exmaple.org',
                first_name='',
                password='foobar'
            )
        with self.assertRaises(ValueError):
            user_model.objects.create_superuser(
                email='super3@exmaple.org',
                first_name='Super',
                password=''
            )
