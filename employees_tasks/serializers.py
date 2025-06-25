from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Employee, Task

from random import choices
import string



class EmployeeSerializer(serializers.ModelSerializer):
  username = serializers.CharField(write_only=True)  # имя пользователя
  generated_password = serializers.CharField(
    read_only=True, min_length=6, max_length=6
  )

  class Meta:
    model = Employee
    fields = ['id', 'full_name', 'position', 'username', 'generated_password']

  def create(self, validated_data):
    username = validated_data.pop('username')

    # генерируем простой 6-символьный пароль
    password = ''.join(choices(string.ascii_lowercase + string.digits, k=6))

    # создаём пользователя
    user = User(username=username)
    user.set_password(password)
    user.save()

    # создаём сотрудника, связанного с этим пользователем
    employee = Employee.objects.create(user=user, **validated_data)

    # добавляем сгенерированный пароль к объекту (для to_representation)
    employee._generated_password = password
    return employee

  def to_representation(self, instance):
    data = super().to_representation(instance)
    if hasattr(instance, '_generated_password'):
      data['generated_password'] = instance._generated_password
    return data



class TaskSerializer(serializers.ModelSerializer):
  employee_name = serializers.CharField(
    source='employee.full_name',
    read_only=True
  )

  class Meta:
    model = Task
    fields = [
      'id', 'title', 'parent_task', 'employee', 'employee_name',
      'deadline', 'status'
    ]
