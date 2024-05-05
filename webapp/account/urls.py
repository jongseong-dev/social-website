from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # 직접 만든 로그인 뷰
    # path("login/", views.user_login, name="login"),
    # 로그인 / 로그아웃
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # 패스워드 변경
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("", views.dashboard, name="dashboard"),
]
