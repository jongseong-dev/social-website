import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from exceptions import InvalidImageException
from images.models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput,  # type=hidden input 요소로 랜더링
        }

    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_extensions = ["jpg", "jpeg", "png"]
        extension = url.rsplit(".", 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given URL does not match valid image extensions."
            )
        return url

    def save(self, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data["url"]
        name = slugify(image.title)
        extension = image_url.rsplit(".", 1)[1].lower()
        image_name = f"{name}.{extension}"

        try:
            response = requests.get(image_url, timeout=10)  # 타임아웃 설정
            response.raise_for_status()  # 200 OK 응답이 아니면 에러 발생
        except (requests.RequestException, ValueError):
            # request 에러 또는 잘못된 URL에 대한 처리
            raise InvalidImageException("Could not download the image.")

        # Content-Type이 이미지인지 확인
        if "image" not in response.headers["Content-Type"]:
            raise InvalidImageException("Not a valid image file.")

        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:
            image.save()
        return image
