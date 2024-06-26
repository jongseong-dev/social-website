import redis
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from actions.utils import create_action
from exceptions import InvalidImageException
from images.forms import ImageCreateForm
from images.models import Image

r = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


@login_required
def image_create(request):
    try:
        if request.method == "POST":
            form = ImageCreateForm(data=request.POST)
            if form.is_valid():
                new_image = form.save(commit=False)
                new_image.user = request.user
                new_image.save()
                create_action(request.user, "bookmarked image", new_image)
                messages.success(request, "Image added successfully")
                return redirect(
                    new_image.get_absolute_url()
                )  # 새로 생성된 이미지 상세 뷰로 리디렉션
    except (InvalidImageException, ValidationError) as e:
        messages.error(request, e.message)
        pass
    form = ImageCreateForm(data=request.GET)
    return render(
        request,
        "images/image/create.html",
        {"section": "images", "form": form},
    )


def image_detail(request, pk, slug):
    image = get_object_or_404(Image, pk=pk, slug=slug)
    # 이미지의 총 조회수가 1씩 증가
    total_views = r.incr(
        f"image:{image.id}:views"
    )  # object-type:id:field 형태로 저장
    # 이미지 순위가 1씩 증가
    r.zincrby("image_ranking", 1, image.id)
    return render(
        request,
        "images/image/detail.html",
        {"section": "images", "image": image, "total_views": total_views},
    )


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action in ["like", "unlike"]:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse("")
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            "images/image/list_images.html",
            {"section": "images", "images": images},
        )
    return render(
        request,
        "images/image/list.html",
        {"section": "images", "images": images},
    )


@login_required
def image_ranking(request):
    # 이미지 순위 딕셔너리 가져오기
    # zrange 메소드는  조회할 멤버의 시작 인덱스와 끝 인덱스를 필요로 한다.
    image_ranking_list = r.zrange("image_ranking", 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id_) for id_ in image_ranking_list]
    # 가장 많이 조회된 이미지 가져오기
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(
        request,
        "images/image/ranking.html",
        {"section": "images", "most_viewed": most_viewed},
    )
