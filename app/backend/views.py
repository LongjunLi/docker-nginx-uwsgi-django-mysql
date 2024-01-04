from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status

from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from backend.commons.customresponse import CustomResponse
from backend.commons.page import Page
from backend.utils.log import net_log, REQUEST
from backend.serializers import *
from backend.filters import *


class RegisterView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        net_log(request.data, REQUEST)
        username = request.data.get("username")
        if not username:
            return CustomResponse(data=None, code=400, msg="Username cannot be empty!", status=status.HTTP_200_OK)

        password = request.data.get("password")
        if not password:
            return CustomResponse(data=None, code=400, msg="Password cannot be empty!", status=status.HTTP_200_OK)

        self.serializer_class.create(self, request=request)
        return CustomResponse(data=None, code=200, msg="success", status=status.HTTP_200_OK)


class SigninView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SigninSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        net_log(request.data, REQUEST)

        if response.status_code == 200:
            data = {"token": response.data["access"]}
            return CustomResponse(data=data, code=200, msg="success", status=status.HTTP_200_OK)

        return response


class UserInfoCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def post(self, request):
        net_log(request.data, REQUEST)
        self.serializer_class.create(self, request=request)
        return CustomResponse(data=None, code=200, msg="success", status=status.HTTP_200_OK)


class UserInfoUpdateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoSerializer

    def post(self, request):
        net_log(request.data, REQUEST)
        self.serializer_class.update(self, request=request)
        return CustomResponse(data=None, code=200, msg="success", status=status.HTTP_200_OK)


class UserInfoDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoDeleteSerializer

    def post(self, request):
        net_log(request.data, REQUEST)
        self.serializer_class.delete(self, request=request)
        return CustomResponse(data=None, code=200, msg="success", status=status.HTTP_200_OK)


class UserInfoGetView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserInfoGetSerializer

    def get(self, request):
        net_log(request.data, REQUEST)
        queryset = self.serializer_class.list(self, request=request)
        serializer = self.get_serializer(instance=queryset, many=False)
        return CustomResponse(data=serializer.data, code=200, msg="success", status=status.HTTP_200_OK)


class ItemCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer

    def post(self, request):
        net_log(request.data, REQUEST)
        self.serializer_class.create(self, request=request)
        return CustomResponse(data=None, code=200, msg="success", status=status.HTTP_200_OK)


class ItemUpdateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer

    def post(self, request):
        net_log(request.data, REQUEST)
        self.serializer_class.update(self, request=request)
        return CustomResponse(data=None, code=200, msg="success", status=status.HTTP_200_OK)


class ItemDeleteView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer

    def post(self, request):
        net_log(request.data, REQUEST)
        self.serializer_class.delete(self, request=request)
        return CustomResponse(data=None, code=200, msg="success", status=status.HTTP_200_OK)


class ItemListView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ItemFilter
    ordering_fields = ("name",)
    pagination_class = Page

    def get(self, request):
        net_log(request.data, REQUEST)
        queryset = self.serializer_class.list(self, request=request)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset=queryset)
        serializer = self.get_serializer(instance=page, many=True)
        return self.get_paginated_response(serializer.data)
