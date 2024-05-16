from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Post

def post_list(request):
    post_qs = Post.objects.all()
    post_qs = post_qs.select_related("author")
    post_qs = post_qs.prefetch_related("tag_set", "comment_set", "comment_set__author")

    return render(request, "blog/post_list.html", {
        "post_list": post_qs
    })

@login_required
@permission_required("blog.view_post", raise_exception=False)
def post_detail(request : HttpRequest, slug):
    post = get_object_or_404(Post, slug=slug)

    return HttpResponse(f"{post.pk}번 글의 슬러그: {post.slug}")


@login_required
@permission_required("blog.view_premium_post", login_url="blog:premium_user_guide")
def post_premium_detail(request : HttpRequest, slug):
    post = get_object_or_404(Post, slug=slug)

    return HttpResponse(f"프리미엄 컨텐츠 페이지: {post.slug}")


def premium_user_guide(request):
    return HttpResponse("프리미엄 유저 가이드 페이지")

