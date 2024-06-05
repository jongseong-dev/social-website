# 사용자 활동 추적하기

## 기능 목록
- 팔로우 시스템 구축하기
- 중개 모델을 사용해 다대다 관계 만들기
- 활동 스트림 애플리케이션 만들기
- 모델에 일반화한 관계 추가하기
- 관련 객체에 대한 QuerySet 최적화하기
- 카운트 역정규화를 위해 시그널 사용하기
- 장고 디버그 도구 모음을 사용해 관련 디버그 ㅓㅈㅇ보 얻기
- Redis로 이미지 뷰 카운트하기
- Redis로 가장 많이 조회된 이미지의 랭킹 정하기

## 팔로우 시스템 구축하기
- 중개 모델을 사용한 다대다 관계 만들기

## 활동 스트림 앱 구축하기
- 사용자에게 활동 스트림을 표시해서 다른 사용자가 플랫폼에서 수행하는 작업을 추적할 수 있다.
- 활동 스트림은 사용자 또는 사용자 그룹이 수행한 최근 활동의 목록이다.

### contenttypes 프레임워크 사용하기
- 기존의 여러 모델들의 인스턴스를 가리킬 수 있는 방법을 제공한다.
- django.contrib.contenttypes에 contenttypes 프레임워크가 포함되어 있다.
- 이 앱은 프로젝트에 설치된 모든 모델을 추적할 수 있으며, 모델과 상호작용할 수 있는 일반화된 인터페이스를 제공한다.
- ContentType 모델에는 다음과 같은 필드가 있다.
    - app_label: 모델이 속한 앱의 이름을 나타낸다.
    - model: 모델 클ㄹ스의 이름이다.
    - name: 사람이 읽을 수 있는 모델의 이름을 나타낸다

### 활동스트림에서 중복 활동 피하기
- 사용자가 좋아요 또는 싫어요 버튼을 여러 번 클릭하거나 단기간에 동일한 활동을 여러 번 수행할 수 있다.
- 이를 방지하기 위해 중복된 활동을 건너뛰도록 create_action() 함수를 수정한다.
```python
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
```

### 사용자 활동 추가
- 사용자가 이미지를 북마크하는 행동
- 사용자가 이미지에 좋아요를 표시하는 행동
- 사용자가 계정을 만드는 행동
- 사용자가 다른 사용자를 팔로우하기 시작하는 행동

### QuerySet 최적화하기
- Action 객체를 조회할 때마다 관련 User 객체와 사용자의 Profile 객체를 불필요하게 접근하게 된다.
- 이를 피하기 위해 `select_related`를 사용한다.
- select_related는 `FK`와 `OneToOne` 필드를 위한 메서드이다.
- 이 메서드는 **SQL Join**을 수행해서 관련된 객체의 필드들을 SELECT 문에 포함시키는 방식으로 작동한다.
- select_related는 **다대다** 또는 다대일(ManyToMAny 또는 역관계의 FK 필드)에서는 작동하지 않는다.
- `prefetch_related`를 사용해서 각 관계마다 별도로 조회하고 파이썬을 사용해서 결과를 조인한다.
- 이 메서드는 GenericRelation과 GenericForeignKey의 프리패칭도 지원한다.