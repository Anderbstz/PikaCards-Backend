from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Tu API de cartas
    path('api/', include('pikacards.urls')),

    # Tu login/registro personalizados
    path("auth/", include("authapi.urls")),

    # JWT correcto
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/", include("pikacards.urls")),
]