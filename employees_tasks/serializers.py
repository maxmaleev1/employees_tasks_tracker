import random
import string

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Employee, Task


class EmployeeSerializer(serializers.ModelSerializer):
  username = serializers.CharField(write_only=True, required=False)
  generated_password = serializers.CharField(read_only=True)

  class Meta:
    model = Employee
    fields = ['id', 'full_name', 'position', 'username', 'generated_password']

  def create(self, validated_data):
    username = validated_data.pop('username')

    generated_password = ''.join(
      random.choices(string.ascii_letters + string.digits, k=8)
    )

    user = User.objects.create_user(username=username,
                                    password=generated_password)

    employee = Employee.objects.create(user=user, **validated_data)
    employee.generated_password = generated_password
    return employee

  def update(self, instance, validated_data):
    validated_data.pop('username', None)  # игнорировать username при PATCH
    return super().update(instance, validated_data)

  def to_representation(self, instance):
    rep = super().to_representation(instance)
    if hasattr(instance, 'generated_password'):
      rep['generated_password'] = instance.generated_password
    return rep



class TaskSerializer(serializers.ModelSerializer):
  employee_full_name = serializers.CharField(
    source="employee.full_name",
    read_only=True
  )
  parent_task_title = serializers.CharField(
    source="parent_task.title",
    read_only=True,
    default=None
  )
  employee_username = serializers.CharField(
    source="employee.user.username",
    read_only=True
  )

  class Meta:
    model = Task
    fields = [
      "id",
      "title",
      "status",
      "deadline",
      "employee",
      "employee_full_name",
      "employee_username",
      "parent_task",
      "parent_task_title",
    ]

