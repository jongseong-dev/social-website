from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 직접 만든 로그인 뷰
    # path("login/", views.user_login, name="login"),
    # 장고에서 제공하는 인증 뷰
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
