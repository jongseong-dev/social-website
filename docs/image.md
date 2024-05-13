# 이미지 북마크 웹사이트 만들기

## 개요
- 사용자가 다른 웹사이트에서 찾은 이미지를 북마크하고 사이트에서 공유핟조록 허용하는 방법을 알아보자

## 기능을 구축화기 위해 필요한 요소

1. 이미지 및 관련 정보를 저장하는 데이터 모델
2. 이미지 업로드를 처리하는 폼과 뷰
3. JavaScript 북마클릿 코드를 통해 페이지 전체에서 이미지를 찾고 사용자가 북마크하려는 이미지를 선택할 수 있도록 하자.

## 이미지 모델

- slug 필드를 자동으로 생성하기 위해 save() 메서드를 오버라이드한다.
```python
from django.utils.text import slugify
from django.db import models


class Image(models.Model):

    def save(self, *args, **kwargs):
        """
        제목 필드의 값을 기반으로 slug 필드를 자동으로 생성하도록 한다.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

```

## 다른 웹사이트의 콘텐츠 게시하기

### 폼 필드 정리하기

- url 필드의 확장자 validation 확인

```python
from django import forms
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

```