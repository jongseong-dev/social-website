from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from images.form import ImageCreateForm


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added successfully")
            return redirect(
                new_image.get_absolute_url()
            )  # 새로 생성된 이미지 상세 뷰로 리디렉션
    form = ImageCreateForm(data=request.GET)
    return render(
        request,
        "images/image/create.html",
        {"section": "images", "form": form},
    )
