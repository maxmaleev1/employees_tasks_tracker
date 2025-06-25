from django.urls import reverse, resolve
from rest_framework.test import APITestCase

from employees_tasks.views import (
  TaskViewSet,
  EmployeeViewSet
)



class URLTests(APITestCase):
  def test_task_list_url_resolves(self):
    url = reverse('task-list')
    self.assertEqual(resolve(url).func.cls, TaskViewSet)

  def test_task_detail_url_resolves(self):
    url = reverse('task-detail', args=[1])
    self.assertEqual(resolve(url).func.cls, TaskViewSet)

  def test_task_overdue_url_resolves(self):
    url = reverse('task-overdue')
    self.assertEqual(resolve(url).func.cls, TaskViewSet)

  def test_task_important_url_resolves(self):
    url = reverse('task-important')
    self.assertEqual(resolve(url).func.cls, TaskViewSet)

  def test_task_busy_employees_url_resolves(self):
    url = reverse('task-busy-employees')
    self.assertEqual(resolve(url).func.cls, TaskViewSet)

  def test_employee_list_url_resolves(self):
    url = reverse('employee-list')
    self.assertEqual(resolve(url).func.cls, EmployeeViewSet)

  def test_employee_detail_url_resolves(self):
    url = reverse('employee-detail', args=[1])
    self.assertEqual(resolve(url).func.cls, EmployeeViewSet)
