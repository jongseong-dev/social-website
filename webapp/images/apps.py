from django.apps import AppConfig


class ImagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "images"

    def ready(self):  # 시그널을 등록하는 일반적인 방법
        # signal 핸들러 임포트
        import images.signals  # noqa
