from django.urls import path, include

from . import views

urlpatterns = [
    # 직접 만든 로그인 뷰
    # path("login/", views.user_login, name="login"),
    # 로그인 / 로그아웃
    # path("login/", auth_views.LoginView.as_view(), name="login"),
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # # 패스워드 변경
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(),
    #     name="password_change",
    # ),
    # path(
    #     "password-change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(),
    #     name="password_change_done",
    # ),
    # # 패스워드 재설정
    # path(
    #     "password-reset/",
    #     auth_views.PasswordResetView.as_view(),
    #     name="password_reset",
    # ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-reset/complete/",
    #     auth_views.PasswordResetCompleteView.as_view(),
    #     name="password_reset_complete",
    # ),
    path("", include("django.contrib.auth.urls")),  # 장고에서 제공하는 인증 URL include
    path("", views.dashboard, name="dashboard"),
    path("register/", views.register, name="register"),
]
