from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Action(models.Model):
    user = models.ForeignKey(
        "auth.User", related_name="actions", on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="target_obj",
        on_delete=models.CASCADE,
        db_comment="ContentType 모델을 가리키는 FK 필드",
    )
    target_id = models.PositiveIntegerField(
        null=True, blank=True, db_comment="관련 객체의 기본 키를 저장하는 필드"
    )
    target = GenericForeignKey(
        "target_ct", "target_id"
    )  # 해당 필드의 조합을 기반으로 관계된 객체를 가리킨다.

    class Meta:
        indexes = [
            models.Index(fields=["-created"]),
        ]
        ordering = ["-created"]
