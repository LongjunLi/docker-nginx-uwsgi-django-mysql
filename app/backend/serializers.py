from rest_framework import serializers

from django.contrib.auth.backends import ModelBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from backend.commons.customexception import ParamsException
from backend.utils.md5 import calculate_md5
from backend.utils.log import log
from backend.models import *


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=calculate_md5(username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SigninSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(SigninSerializer, cls).get_token(user)

        token["username"] = user.username
        token["is_admin"] = user.is_admin
        token["is_active"] = user.is_active
        return token


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, error_messages={})
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        username_md5 = calculate_md5(username)

        if User.objects.filter(username=username_md5).count():
            log("Username existed!", "UserCreate")
            raise ParamsException({"custom_msg": "Username existed!"})

        user = User.objects.create(username=username_md5)

        user.set_password(password)
        user.save()


class UserInfoSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()

    class Meta:
        model = UserInfo
        fields = ("firstname", "lastname")

    def create(self, request):
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")

        if UserInfo.objects.filter(user_id=request.user.id).count():
            log("User info existed!", "UserInfoCreate")
            raise ParamsException({"custom_msg": "User info existed!"})

        user_info = UserInfo.objects.create(user_id=request.user.id,
                                            firstname=firstname,
                                            lastname=lastname)
        user_info.save()

    def update(self, request):
        firstname = request.data.get("firstname")
        lastname = request.data.get("lastname")

        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except:
            log("User info non-existed!", "UserInfoUpdate")
            raise ParamsException({"custom_msg": "User info non-existed!"})

        user_info.firstname = firstname
        user_info.lastname = lastname
        user_info.save()


class UserInfoDeleteSerializer(serializers.ModelSerializer):

    def delete(self, request):
        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except:
            log("User info non-existed!", "UserInfoDelete")
            raise ParamsException({"custom_msg": "User info non-existed!"})
        user_info_delete = UserInfoDelete.objects.create(user_id=user_info.user_id,
                                                         user_info_id=user_info.id,
                                                         firstname=user_info.firstname,
                                                         lastname=user_info.lastname)
        user_info_delete.save()
        user_info.delete()


class UserInfoGetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    firstname = serializers.CharField(read_only=True)
    lastname = serializers.CharField(read_only=True)
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserInfo
        fields = ("id", "user_id", "firstname", "lastname", "create_time", "update_time")

    def list(self, request):
        try:
            user_info = UserInfo.objects.get(user_id=request.user.id)
        except:
            log("User info non-existed!", "UserInfoGet")
            raise ParamsException({"custom_msg": "User info non-existed!"})
        return user_info


class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    create_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Item
        fields = ("id", "name", "create_time", "update_time")

    def create(self, request):
        name = request.data.get("name")

        item = Item.objects.create(name=name)
        item.save()

    def update(self, request):
        id = request.data.get("id")
        name = request.data.get("name")

        try:
            item = Item.objects.get(id=id)
        except:
            log("Item non-existed!", "ItemUpdate")
            raise ParamsException({"custom_msg": "Item non-existed!"})

        item.name = name
        item.save()

    def delete(self, request):
        id = request.data.get("id")

        try:
            item = Item.objects.get(id=id)
        except:
            log("Item non-existed!", "ItemDelete")
            raise ParamsException({"custom_msg": "Item non-existed!"})
        item_delete = ItemDelete.objects.create(item_id=item.id,
                                                operate_user_id=request.user.id,
                                                name=item.name)
        item_delete.save()
        item.delete()

    def list(self, request):
        items = Item.objects.filter()
        return items


class UploadFilesSerializer(serializers.ModelSerializer):
    file = serializers.FileField()


class SendEmailSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
