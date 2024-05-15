from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Post

def post_detail(request : HttpRequest, slug):
    post = get_object_or_404(Post, slug=slug)

    return HttpResponse(f"{post.pk}번 글의 슬러그: {post.slug}")