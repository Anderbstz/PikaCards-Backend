from django.contrib import admin
from django.urls import path, include

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# IMPORTANTE: necesitas importar ai_chat
from pikacards.views import ai_chat


urlpatterns = [
    path('admin/', admin.site.urls),

    # API de PikaCards
    path('api/', include('pikacards.urls')),

    # Login / Registro
    path("auth/", include("authapi.urls")),

    # JWT Tokens
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Chatbot endpoint
    path("api/ai-chat/", ai_chat),
]
