from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.Роль == "admin" or user.Роль == "manager":
            users = get_user_model().objects.all()
        elif user.Роль == "user":
            users = get_user_model().objects.filter(Организация=user.Организация)
        else:
            return Response(
                {"detail": "Недостаточно прав для просмотра."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.Роль != "admin":
            raise PermissionDenied("У вас нет прав на создание пользователя.")

        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Пользователь создан",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            user = get_user_model().objects.get(id=pk)
        except get_user_model().DoesNotExist:
            raise NotFound("Пользователь не найден.")

        if request.user.Роль == "user" and request.user.id != user.id:
            raise PermissionDenied("Вы не можете редактировать чужой профиль.")

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Пользователь обновлен",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
