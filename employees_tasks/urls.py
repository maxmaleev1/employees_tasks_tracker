from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import TaskViewSet, EmployeeViewSet
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)

# создаём роутер и регистрируем оба ViewSet'а
router = SimpleRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'employees', EmployeeViewSet, basename='employee')

# объединяем маршруты
urlpatterns = router.urls + [
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
