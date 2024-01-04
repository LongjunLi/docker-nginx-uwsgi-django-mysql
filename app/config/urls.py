from django.urls import path

from backend.views import *


urlpatterns = [
    path("apis/Register/", RegisterView.as_view()),
    path("apis/Signin/", SigninView.as_view()),
    path("apis/UserInfoCreate/", UserInfoCreateView.as_view()),
    path("apis/UserInfoUpdate/", UserInfoUpdateView.as_view()),
    path("apis/UserInfoDelete/", UserInfoDeleteView.as_view()),
    path("apis/UserInfoGet/", UserInfoGetView.as_view()),
    path("apis/ItemCreate/", ItemCreateView.as_view()),
    path("apis/ItemUpdate/", ItemUpdateView.as_view()),
    path("apis/ItemDelete/", ItemDeleteView.as_view()),
    path("apis/ItemList/", ItemListView.as_view()),
]
