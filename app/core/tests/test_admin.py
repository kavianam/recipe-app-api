from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user: User = get_user_model().objects.create_superuser(
            email='kavianam@gmail.com',
            password='test1234'
        )
        # self.client.login(email='kavianam@gmail.com', password='test1234')
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test1234',
            name='test1'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        # /admin/core/user/
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # /admin/core/user/id
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user works"""
        url = reverse('admin:core_user_add')
        # /admin/core/user/add
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_login(self):
        self.assertTrue(self.admin_user.is_authenticated)
