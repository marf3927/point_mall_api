from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.generics import mixins, GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from item.serializers import UserItemSerializer

from .models import User
from .serializers import UserSerializer


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MyItemsView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserItemSerializer(request.user.items.all(), many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True)
    def items(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserItemSerializer(user.items.all(), many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
            password = make_password(self.request.data['password'])
        )
