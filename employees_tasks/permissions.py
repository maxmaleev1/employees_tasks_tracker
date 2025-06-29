from rest_framework.permissions import BasePermission, SAFE_METHODS



class IsAdminOrReadOnly(BasePermission):
  '''
  Изменять и удалять может только админ (is_staff=True),
  остальные могут только просматривать.
  '''

  def has_permission(self, request, view):
    return (request.method in SAFE_METHODS or request.user.is_staff)



class IsAssignedEmployeeOrReadOnly(BasePermission):
  '''
  Изменение задачи (PATCH/PUT) разрешено только назначенному исполнителю.
  '''

  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
      return True

    return obj.employee.user == request.user


class CustomTaskPermission(BasePermission):
  '''
  Права доступа:
  - Создавать задачи может только админ.
  - Удалять задачи может только админ, и только если задача завершена.
  - Изменять задачи может только назначенный исполнитель.
  '''
  def has_permission(self, request, view):
    if view.action == 'create':
      return request.user.is_staff
    if view.action == 'destroy':
      return request.user.is_staff
    if view.action in ['update', 'partial_update']:
      return True  # проверка в has_object_permission
    return True

  def has_object_permission(self, request, view, obj):
    if request.method in SAFE_METHODS:
      return True

    if view.action in ['update', 'partial_update']:
      return obj.employee.user == request.user

    if view.action == 'destroy':
      return obj.status == 'completed' and request.user.is_staff

    return False
