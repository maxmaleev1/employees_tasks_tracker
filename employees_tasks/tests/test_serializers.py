from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from rest_framework.test import APITestCase

from employees_tasks.models import Employee, Task
from employees_tasks.serializers import TaskSerializer, EmployeeSerializer



class TaskSerializerTests(APITestCase):
  def test_employee_name_is_included(self):
    user = User.objects.create_user(username='testuser', password='123456')
    employee = Employee.objects.create(
      user=user, full_name='Test User', position='Dev'
    )
    task = Task.objects.create(
      title='Test Task',
      deadline=now() + timedelta(days=1),
      status='not_started',
      employee=employee
    )

    serializer = TaskSerializer(task)
    self.assertEqual(serializer.data['employee_name'], 'Test User')



class EmployeeSerializerTests(APITestCase):
  def test_employee_created_with_generated_password(self):
    data = {
      'username': 'genuser',
      'full_name': 'Generated Emp',
      'position': 'QA'
    }

    serializer = EmployeeSerializer(data=data)
    self.assertTrue(serializer.is_valid(), serializer.errors)

    employee = serializer.save()

    # пользователь создан
    self.assertTrue(User.objects.filter(username='genuser').exists())

    # пароль задан
    self.assertTrue(employee.user.check_password(employee._generated_password))

    # сериализация включает сгенерированный пароль
    rep = serializer.to_representation(employee)
    self.assertIn('generated_password', rep)
    self.assertEqual(len(rep['generated_password']), 6)
