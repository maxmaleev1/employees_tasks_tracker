from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from employees_tasks.models import Task, Employee
from employees_tasks.permissions import (
  IsAdminOrReadOnly,
  IsAssignedEmployeeOrReadOnly,
)


class PermissionsTests(APITestCase):

  def setUp(self):
    self.factory = APIRequestFactory()

    self.admin_user = User.objects.create_user(
      username='admin', password='pass', is_staff=True
    )
    self.admin_employee = Employee.objects.create(
      user=self.admin_user, full_name='Admin Name'
    )

    self.user = User.objects.create_user(username='user', password='pass')
    self.employee = Employee.objects.create(
      user=self.user, full_name='User Name'
    )

  def test_only_admin_can_delete_task(self):
    task = Task.objects.create(
      title='Test Task',
      employee=self.employee,
      deadline=timezone.now() + timedelta(days=1)
    )

    perm = IsAdminOrReadOnly()

    # обычный пользователь
    request = self.factory.delete('/')
    request.user = self.user
    self.assertFalse(perm.has_permission(request, None))

    # админ
    request = self.factory.delete('/')
    request.user = self.admin_user
    self.assertTrue(perm.has_permission(request, None))

  def test_only_assigned_can_update_task(self):
    task = Task.objects.create(
      title='Test Task',
      employee=self.employee,
      deadline=timezone.now() + timedelta(days=1)
    )

    perm = IsAssignedEmployeeOrReadOnly()

    # не назначенный пользователь
    other_user = User.objects.create_user(username='other', password='pass')
    request = self.factory.patch('/')
    request.user = other_user
    self.assertFalse(perm.has_object_permission(request, None, task))

    # назначенный пользователь
    request = self.factory.patch('/')
    request.user = self.user
    self.assertTrue(perm.has_object_permission(request, None, task))

  def test_safe_methods_allowed_for_all(self):
    task = Task.objects.create(
      title='Test Task',
      employee=self.employee,
      deadline=timezone.now() + timedelta(days=1)
    )

    perm = IsAssignedEmployeeOrReadOnly()

    request = self.factory.get('/')
    request.user = self.user
    self.assertTrue(perm.has_object_permission(request, None, task))

  def test_safe_methods_allowed_for_all_in_object_permission(self):
    task = Task.objects.create(
      title='Test Task',
      employee=self.employee,
      deadline=timezone.now() + timedelta(days=1)
    )

    perm = IsAssignedEmployeeOrReadOnly()

    request = self.factory.options('/')
    request.user = self.admin_user
    self.assertTrue(perm.has_object_permission(request, None, task))

  def test_other_methods_fallthrough_returns_true(self):
    task = Task.objects.create(
      title='Test Task',
      employee=self.employee,
      deadline=timezone.now() + timedelta(days=1)
    )

    class DummyRequest:
      method = 'DELETE'
      user = self.user

    perm = IsAssignedEmployeeOrReadOnly()
    self.assertTrue(perm.has_object_permission(DummyRequest(), None, task))
