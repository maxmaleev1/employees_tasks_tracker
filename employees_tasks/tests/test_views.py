from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils.timezone import now, timedelta

from employees_tasks.models import Task, Employee



class TaskViewSetTests(APITestCase):
  def setUp(self):
    self.admin_user = User.objects.create_user(
      username='admin', password='adminpass', is_staff=True
    )
    self.admin_employee = Employee.objects.create(
      user=self.admin_user, full_name='Admin', position='Manager'
    )

    self.employee_user = User.objects.create_user(
      username='user', password='pass'
    )
    self.employee = Employee.objects.create(
      user=self.employee_user, full_name='User', position='Dev'
    )

    self.task = Task.objects.create(
      title='Main Task',
      deadline=now() + timedelta(days=2),
      status='not_started',
      employee=self.employee
    )

    self.client = APIClient()

  def test_task_list_authenticated(self):
    self.client.force_authenticate(user=self.employee_user)
    response = self.client.get('/employees_tasks/tasks/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_task_delete_only_admin(self):
    self.client.force_authenticate(user=self.employee_user)
    response = self.client.delete(f'/employees_tasks/tasks/{self.task.id}/')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    self.client.force_authenticate(user=self.admin_user)
    response = self.client.delete(f'/employees_tasks/tasks/{self.task.id}/')
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

  def test_task_update_only_assigned(self):
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.patch(
      f'/employees_tasks/tasks/{self.task.id}/',
      {'status': 'in_progress'},
      format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    self.client.force_authenticate(user=self.employee_user)
    response = self.client.patch(
      f'/employees_tasks/tasks/{self.task.id}/',
      {'status': 'in_progress'},
      format='json'
    )
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_overdue_tasks(self):
    overdue_task = Task.objects.create(
      title='Overdue',
      deadline=now() - timedelta(days=1),
      status='not_started',
      employee=self.employee
    )
    self.client.force_authenticate(user=self.employee_user)
    response = self.client.get('/employees_tasks/tasks/overdue/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.data), 1)

  def test_important_tasks(self):
    important = Task.objects.create(
      title='Important',
      deadline=now() + timedelta(days=5),
      status='not_started',
      employee=self.employee
    )
    self.client.force_authenticate(user=self.employee_user)
    response = self.client.get('/employees_tasks/tasks/important/')
    self.assertEqual(response.status_code, 200)
    self.assertGreaterEqual(len(response.data), 1)

  def test_busy_employees(self):
    Task.objects.create(
      title='T2',
      deadline=now() + timedelta(days=5),
      status='in_progress',
      employee=self.employee
    )
    self.client.force_authenticate(user=self.admin_user)
    response = self.client.get('/employees_tasks/tasks/busy_employees/')
    self.assertEqual(response.status_code, 200)
    self.assertGreaterEqual(len(response.data), 1)

  def test_unauthenticated_cannot_access(self):
    response = self.client.get('/employees_tasks/tasks/')
    self.assertEqual(response.status_code, 401)



class EmployeeViewSetTests(APITestCase):
  def setUp(self):
    self.admin_user = User.objects.create_user(
      username='admin', password='adminpass', is_staff=True
    )
    self.admin_employee = Employee.objects.create(
      user=self.admin_user, full_name='Admin', position='Boss'
    )

    self.employee_user = User.objects.create_user(
      username='user', password='pass'
    )
    self.employee = Employee.objects.create(
      user=self.employee_user, full_name='User', position='Dev'
    )

    self.client = APIClient()

  def test_list_employees(self):
    self.client.force_authenticate(user=self.employee_user)
    response = self.client.get('/employees_tasks/employees/')
    self.assertEqual(response.status_code, 200)

  def test_create_employee_only_admin(self):
    self.client.force_authenticate(user=self.employee_user)
    response = self.client.post('/employees_tasks/employees/', {
      'username': 'newguy',
      'full_name': 'New Guy',
      'position': 'Tester'
    }, format='json')
    self.assertEqual(response.status_code, 403)

    self.client.force_authenticate(user=self.admin_user)
    response = self.client.post('/employees_tasks/employees/', {
      'username': 'newguy',
      'full_name': 'New Guy',
      'position': 'Tester'
    }, format='json')
    self.assertEqual(response.status_code, 201)
    self.assertIn('generated_password', response.data)
