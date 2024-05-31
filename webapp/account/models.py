from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class Contact(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rel_from_set",
        on_delete=models.CASCADE,
    )  # 관계를 만드는  FK
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="rel_to_set",
        on_delete=models.CASCADE,
    )  # 팔로우 되는 사용자에 관한 FK
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["-created"])]
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"


# User에 다음 필드를 동적으로 추가
user_model = get_user_model()
user_model.add_to_class(  # add_to_class는 권장하는 방법이 아님
    # 그러나 이 경우 이 메서드를 사용하면 커스텀 사용자 모델을 만들지 않고도
    # 장고가 기본으로 제공하는 User모델의 모든 이점을 유지할 수 있다.
    "following",
    models.ManyToManyField(
        "self",
        through=Contact,  # 중개 모델을 지정
        related_name="followers",
        symmetrical=False,  # ManyToManyField의 대칭성을 제거
        # -> 내가 누군가를 팔로우 했다고 자동으로 그가 나를 팔로우하는 것은 아니다.
    ),
)
