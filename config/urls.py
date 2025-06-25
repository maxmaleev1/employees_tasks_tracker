from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
  SpectacularAPIView,
  SpectacularSwaggerView,
  SpectacularRedocView
)

from rest_framework_simplejwt.views import (
  TokenObtainPairView,       # выдача access/refresh токенов
  TokenRefreshView           # обновление access токена
)

urlpatterns = [
  path('admin/', admin.site.urls),  # маршрут к админке

  path('employees_tasks/', include('employees_tasks.urls')),  # основное API

  # JWT-маршруты
  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

  # документация и схема
  path('schema/', SpectacularAPIView.as_view(), name='schema'),
  path('schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
       name='swagger-ui'),
  path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'),
       name='redoc'),
]
