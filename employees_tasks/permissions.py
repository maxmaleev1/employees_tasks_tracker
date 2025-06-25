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
