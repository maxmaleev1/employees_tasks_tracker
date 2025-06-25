from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils.timezone import now
from django.db.models import Count

from .models import Task, Employee
from .serializers import TaskSerializer, EmployeeSerializer
from .permissions import (
    IsAdminOrReadOnly,
    IsAssignedEmployeeOrReadOnly,
)



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAdminOrReadOnly()]
        if self.action in ['update', 'partial_update']:
            return [IsAssignedEmployeeOrReadOnly()]
        return super().get_permissions()

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        overdue_tasks = Task.objects.filter(
            deadline__lt=now(),
            status__in=['not_started', 'in_progress'],
        )
        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def important(self, request):
        important_tasks = Task.objects.filter(
            status='not_started',
            subtasks__isnull=True,
        )
        serializer = self.get_serializer(important_tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def busy_employees(self, request):
        busy = (
            Employee.objects.annotate(task_count=Count('tasks'))
            .order_by('-task_count')
        )
        serializer = EmployeeSerializer(busy, many=True)
        return Response(serializer.data)



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAdminOrReadOnly()]
        return super().get_permissions()
