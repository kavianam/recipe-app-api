from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import validators


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email successful"""
        email = 'test@kavianam.ir'
        password = 'Test1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalize(self):
        """Test the email for a new user is normalize"""
        email = "kavian@KAVINAM.IR"
        user = get_user_model().objects.create_user(email, 'test1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_none_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_new_user_invalid_email(self):
        """Test creating user with not valid email raises error"""
        with self.assertRaises(validators.ValidationError):
            get_user_model().objects.create_user("fds", 'test1234')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        email = "kavian@gmail.com"
        password = "Test123"
        user = get_user_model().objects.create_superuser(email, password)
        self.assertEqual(email, user.email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(password))

    def test_new_superuser2(self):
        """Test creating a new superuser"""
        email = "kavian@gmail.com"
        password = "Test123"
        user = get_user_model().objects.create_superuser(email, password, is_staff=False, is_superuser=False)
        self.assertEqual(email, user.email)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.check_password(password))
