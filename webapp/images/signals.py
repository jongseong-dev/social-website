from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from images.models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    """
    Image 모델의 users_like 필드가 변경될 때 호출된다.
    """
    instance.total_likes = instance.users_like.count()
    instance.save()
