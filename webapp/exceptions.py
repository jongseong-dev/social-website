from django.core.exceptions import ValidationError


class InvalidImageException(ValidationError):
    """
    유효하지 이미지 형식일 때 발생하는 예외
    """

    pass
