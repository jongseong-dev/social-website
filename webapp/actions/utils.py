from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from actions.models import Action


def create_action(user, verb, target=None):
    # 마지막 순간에 비슷한 활동이 있었는지 확인
    now = timezone.now()
    last_minute = now - timezone.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id, verb=verb, created__gte=last_minute
    )
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct, target_id=target.id
        )
    if not similar_actions:
        # 존재하는 활동이 발견되지 않은 경우
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True

    return False
