from rest_framework.routers import SimpleRouter

from .views import TaskViewSet, EmployeeViewSet

from .views import CurrentUserView
from django.urls import path


# создаём роутер и регистрируем оба ViewSet'а
router = SimpleRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'employees', EmployeeViewSet, basename='employee')

# объединяем маршруты
urlpatterns = router.urls + [
    path('current_user/', CurrentUserView.as_view(), name='current-user'),
]
