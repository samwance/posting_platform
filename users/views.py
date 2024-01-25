from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import status

from .models import User
from .permissions import IsProfileOwner
from .serializers import UserSerializer


class UserList(generics.ListAPIView):
    """
    List of all users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticated]


class UserCreate(generics.CreateAPIView):
    """
    Create a new user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = User.objects.create(
            phone_number=self.request.data.get("phone_number"),
            is_superuser=False,
            is_staff=False,
            is_active=True,
            username=self.request.data.get("username"),
            birth_date=self.request.data.get("birth_date"),
            email=self.request.data.get("email"),
        )

        user.set_password(self.request.data.get("password"))
        user.save()


class UserDetail(generics.RetrieveAPIView):
    """
    Detailed information about the user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.IsAdminUser]


class UserUpdate(generics.UpdateAPIView):
    """
    Update user information.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileOwner | permissions.IsAdminUser]

    def get_object(self):
        user = self.get_queryset().get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, user)
        return user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        if user != request.user and not request.user.is_staff:
            return Response(
                {"message": "You do not have permission to edit this user."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.update(request, *args, **kwargs)


class UserDelete(generics.DestroyAPIView):
    """
    Delete user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_staff:
            return Response(
                {"message": "You do not have permission to delete this user."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.destroy(request, *args, **kwargs)
