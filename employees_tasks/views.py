from django.utils.timezone import now
from django.db.models import Count, Q

from django.shortcuts import render

from .permissions import (
    IsAdminOrReadOnly,
    IsAssignedEmployeeOrReadOnly, CustomTaskPermission,
)

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Task, Employee
from .serializers import TaskSerializer, EmployeeSerializer

from django.contrib.auth.models import User

from rest_framework.views import APIView


def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    return render(request, 'login.html')

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [CustomTaskPermission]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_staff:
            # Сотрудник может менять только статус
            status = request.data.get('status')
            if status not in ['not_started', 'in_progress', 'completed']:
                return Response({'detail': 'Можно изменить только статус.'},
                                status=400)
            instance.status = status
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({'detail': 'Админ не может редактировать задачи.'},
                        status=403)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Только админ может создавать задачи.'},
                            status=403)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_staff:
            # Сотрудник может менять только статус
            status = request.data.get('status')
            if status not in ['not_started', 'in_progress', 'completed']:
                return Response({'detail': 'Можно изменить только статус.'},
                                status=400)
            instance.status = status
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({'detail': 'Админ не может редактировать задачи.'},
                        status=403)

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

    @action(detail=False, methods=['get'])
    def suitable_employees(self, request):
        parent_task_id = request.query_params.get('parent_task')
        employees = Employee.objects.annotate(
            active_tasks=Count('tasks', filter=Q(tasks__status__in=['not_started', 'in_progress']))
        )
        min_count = employees.aggregate(min_tasks=Count('tasks'))['min_tasks'] or 0

        result = []

        if parent_task_id:
            try:
                parent = Task.objects.get(id=parent_task_id)
            except Task.DoesNotExist:
                return Response({'detail': 'Родительская задача не найдена.'}, status=400)

            parent_employee = parent.employee
            parent_employee_tasks = parent_employee.tasks.filter(
                status__in=['not_started', 'in_progress']
            ).count()

            if parent_employee_tasks <= min_count + 2:
                result.append(parent_employee)

        # Добавляем всех с минимальной загрузкой
        suitable = employees.filter(active_tasks=min_count)
        result.extend(suitable.exclude(id__in=[e.id for e in result]))

        serializer = EmployeeSerializer(result, many=True)
        return Response(serializer.data)


class EmployeeViewSet(viewsets.ModelViewSet):
  queryset = Employee.objects.filter(user__is_staff=False)
  serializer_class = EmployeeSerializer
  permission_classes = [IsAdminOrReadOnly]

  def create(self, request, *args, **kwargs):
    if not request.user.is_staff:
      return Response({'detail': 'Только админ может создавать сотрудников.'},
                      status=403)

    full_name = request.data.get('full_name')
    position = request.data.get('position')
    username = request.data.get('username')

    if not all([full_name, position, username]):
      return Response({'detail': 'Все поля обязательны.'}, status=400)

    import random
    import string
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    user = User.objects.create_user(username=username, password=password)
    employee = Employee.objects.create(user=user,
                                       full_name=full_name,
                                       position=position)

    serializer = self.get_serializer(employee)
    data = serializer.data
    data['generated_password'] = password
    return Response(data, status=201)

  def perform_destroy(self, instance):
      user = instance.user
      instance.delete()
      user.delete()

  @action(detail=False, methods=['get'])
  def busy(self, request):
      employees = (
          Employee.objects.prefetch_related('tasks')
          .annotate(
              active_tasks=Count(
                  'tasks',
                  filter=Q(tasks__status__in=['not_started', 'in_progress'])
              )
          )
          .filter(active_tasks__gt=0)
          .order_by('-active_tasks')
      )
      data = []
      for emp in employees:
          tasks = [
              {'title': t.title, 'status': t.status}
              for t in emp.tasks.all()
              if t.status in ['not_started', 'in_progress']
          ]
          data.append({
              'full_name': emp.full_name,
              'tasks': tasks
          })
      return Response(data)



class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'employee') and request.user.employee:
            full_name = request.user.employee.full_name
        else:
            full_name = ''
        return Response({
            'username': request.user.username,
            'full_name': full_name,
            'is_staff': request.user.is_staff
        })
