from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario creado correctamente"}, status=201)

    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Se requieren credenciales"}, status=400)

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login correcto",
            "user": {
                "username": user.username,
                "email": user.email,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
    else:
        return Response({"error": "Credenciales inválidas"}, status=400)


@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout exitoso"}, status=200)
    except Exception:
        return Response({"error": "Token inválido"}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response({"error": "Se requieren contraseña actual y nueva"}, status=400)

    user_auth = authenticate(username=user.username, password=current_password)
    if user_auth is None:
        return Response({"error": "La contraseña actual es incorrecta"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Contraseña actualizada correctamente"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    confirm = request.data.get('confirm')
    password = request.data.get('password')

    if confirm != 'DELETE':
        return Response({"error": "Confirma escribiendo DELETE"}, status=400)

    if not password:
        return Response({"error": "Proporciona tu contraseña"}, status=400)

    user_auth = authenticate(username=user.username, password=password)
    if user_auth is None:
        return Response({"error": "Contraseña inválida"}, status=400)

    user.delete()
    return Response({"message": "Cuenta eliminada"}, status=200)