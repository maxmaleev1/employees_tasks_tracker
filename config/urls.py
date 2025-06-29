from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
  SpectacularAPIView,
  SpectacularSwaggerView,
  SpectacularRedocView
)

from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from employees_tasks import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_view, name='login'),  # страница логина
    path('main/', views.index_view, name='index'),  # главная страница с index.html
    path('admin/', admin.site.urls),
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

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
