# 이미지 북마크 웹사이트 만들기

<!-- TOC -->
* [이미지 북마크 웹사이트 만들기](#이미지-북마크-웹사이트-만들기)
  * [개요](#개요)
  * [기능을 구축화기 위해 필요한 요소](#기능을-구축화기-위해-필요한-요소)
  * [이미지 모델](#이미지-모델)
  * [다른 웹사이트의 콘텐츠 게시하기](#다른-웹사이트의-콘텐츠-게시하기)
    * [폼 필드 정리하기](#폼-필드-정리하기)
  * [Javascript로 북마클릿 만들기](#javascript로-북마클릿-만들기)
    * [시나리오](#시나리오)
  * [이미지 썸네일 만들기](#이미지-썸네일-만들기)
  * [비동기 액션 추가하기](#비동기-액션-추가하기)
    * [domready](#domready)
  * [이미지 목록에 무한 스크롤 페이징](#이미지-목록에-무한-스크롤-페이징)
    * [crop option](#crop-option-)
    * [무한 스크롤 코드](#무한-스크롤-코드-)
  * [카운트 역정규화를 위한 시그널 사용하기](#카운트-역정규화를-위한-시그널-사용하기)
    * [시그널로 작업하기](#시그널로-작업하기)
    * [좋아요 역정규화](#좋아요-역정규화)
<!-- TOC -->

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

- url로 image 다운해서 저장하기

```python
import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from images.models import Image


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["title", "url", "description"]
        widgets = {
            "url": forms.HiddenInput,  # type=hidden input 요소로 랜더링
        }
    ...

    def save(self, commit=True):
        """
        이미지를 request 모듈을 사용해 내려받아 저장한다.
        Args:
            commit:

        Returns:

        """
        ...
        response = requests.get(image_url)  # 이미지를 내려받는다.
        ...

```

## Javascript로 북마클릿 만들기

- 북마클릿은 웹브라우저에 저장되는 북마크로 JavaScript 코드를 포함해 브라우저의 기능을 확장할 수 있다.
- 브라우저의 북마크나 즐겨찾기 바에서 북마클릿을 클릭하면, 해당 웹사이트에서 JavaScript 코드를 실행할 수 있다.

### 시나리오

1. 사용자가 사이트에서 브라우저의 북마크 바로 링크를 드래그 한다.
2. 링크의 href 속성에는 JavaScript 코드가 포함되어 있다. 이 코드는 북마크에 저장된다.
3. 사용자가 웹사이트를 탐색하고 북마크 또는 즐겨찾기 모음에서 북마크를 클릭한다. 북마크의 JavaScript 코드가 실행된다.

- 주의할 점
    - JavaScript 코드는 북마크로 저장되므로 사용자가 북마크 바에 추가한 후에는 업데이트 할 수 없다. 
    - 이는 런처 스크립트를 구현해서 해결할 수 있다.


## 이미지 썸네일 만들기
- easy-thumbnails 라이브러리를 이용해서 사용자의 썸네일 만들기

## 비동기 액션 추가하기
- 이미지 상세 페이지에 사용자가 like버튼을 누를 경우 비동기로 처리하기

### domready
```javascript
// base.html

document.addEventListener("DOMContentLoaded", (event) => {
        {% block domready %}
        {% endblock %}
    })
```
- DOM이 준비되면 실행되는 핸들러 안에는(`DOMContentLoaded`) domready라는 장고 템플릿 블록이 추가되어 있다.
- base.html 템플릿을 확장한 모든 템플릿은 이 블록을 사용해서 DOM이 준비되었을 때 실행할 특정 JavaScript 코드를 포함할 수 있다.

## 이미지 목록에 무한 스크롤 페이징

- AJAX를 사용하여 무한 스크롤 페이징을 만들어보자
### crop option 

 - crop = smart 은 엔트로피가 낮은 가장자리 부분을 제거해서 점진적으로 이미지를 요청된 크기로 자르라는 의미

`{% thumbnail image.image 300x300 crop="smart" as im %}`

### 무한 스크롤 코드 

```js

  var page = 1; // 현재 페이지 번호를 저장
  var emptyPage = false;
  var blockRequest = false;

  window.addEventListener('scroll', function(e) {  // scroll 이벤트를 캡처하고 이에 대한 핸들러 함수를 정의
    // 문서의 전체 높이와 윈도우 내부 톺이의 차이를 구한다. 구한 값은 사용자가 스크롤 할 수 있는 문서의 남은 높이
    // 이 높이가 200 픽셀에 가까워지면 페이지를 로드할 수 있도록 구한 값에서 200을 뺸다.
    var margin = document.body.clientHeight - window.innerHeight - 200;

    // 오프셋이 계산된 margin보다 큰지 확인
    // 마지막 페이지에 도달한 것은 아닌지 확인
    // 진행 중인 다른 HTTP 요청은 없는지 확인한다.
    if(window.pageYOffset > margin && !emptyPage && !blockRequest) {
      blockRequest = true; // 추가 HTTP 요청을 발생시키지 않도록 true 로 설정
      page += 1;

      fetch('?images_only=1&page=' + page)  // 전체 HTML 페이지 대신 이미지에 대한 HTML과 요청된 페이지 번호에 대한 페이지만 조회한다.
      .then(response => response.text())
      .then(html => {
        if (html === '') {
          // 사용자가 마지막 페이지에 있으며 빈 페이지의 조회 여부를 파악한다. 빈페이지가 조회되면 더 이상 결과가 없는 것으로 간주해서 추가적인 요청을 중지
          emptyPage = true;
        }
        else {
          var imageList = document.getElementById('image-list');
          imageList.insertAdjacentHTML('beforeEnd', html);
          blockRequest = false;
        }
      })
    }
  });

  // Launch scroll event
  const scrollEvent = new Event('scroll');
  window.dispatchEvent(scrollEvent);

```

## 카운트 역정규화를 위한 시그널 사용하기

- 역정규화는 읽기 성능을 최적화하기 위한 방식으로 데이터를 중복으로 만드는 것이다.
- 예를 들어 관계된 데이터를 조회할 때 데이터베이스에 값비싼 읽기 쿼리 요청을 피하기 위해 관련 데이터를 객체에 복사할 수 있다.
- 역정규화의 가장 큰 문제는 역정규화된 데이터를 최신 상태로 유지하기 어렵다는 것이다.

### 시그널로 작업하기

- 장고에는 특정 작업이 발생할 때 수신자 함수가 알림을 받을 수 있는 시그널 디스패치가 함께 제공된다
- 시그널은 어떤 일이 발생할 때마다 코드가 무언가를 수행해야 할 때 유용하다.
- 시그널 메소드
  - `pre_save` : save() 메소드가 호출되기 전에 호출
  - `post_save` : save() 메소드가 호출된 후에 호출
  - `m2m_changed` : ManyToManyField 필드가 변경될 때 호출

### 좋아요 역정규화
- 이미지의 좋아요 총수를 요청마다 계산하는 것은 비효율적이다.
- 따라서 이미지의 좋아요 수를 역정규화 시켜 필드에 넣는다. 

## redis로 이미지 노출 카운트하기
- redis는 다양한 유형의 데이터를 저장할 수 있는 키/값 데이터베이스이다.
- redis는 모든 데이터를 메모리에 저장하지만, 데이터셋을 일정 시간마다 디스크에 덤프하거나 각 명령을 로그에 추가함으로써 영구적으로 저장할 수 이싿.
- 강력한 명령을 제공하고 문자열, 해시, 리스트, 셋, 정렬된 셋 등 다양한 데이터 구조를 지원한다.

### redis 설정하기

- redis는 띄웠다고 가정

- redis 설치하기
```shell
pip install redis
```

- settings.py에 redis 설정 추가하기
```python
# redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
```

- views.py에 redis 사용하기
```python
r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


def image_detail(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, slug=slug)
    # 이미지의 총 조회수가 1씩 증가
    total_views = r.incr(
        f"image:{image.id}:views"
    )  # object-type:id:field 형태로 저장
    return render(
        request,
        "images/image/detail.html",
        {"section": "images", "image": image, "total_views": total_views},
    )
```


## Redis에 랭킹 저장하기
- 정렬된 셋인 `zincrby()` 메소드을 이용하자
- 정렬된 셋은 점수를 가지는 중복되지 않는 문자열 컬렉션을 사용하자
- 요소들은 점수에 따라 정렬된다.