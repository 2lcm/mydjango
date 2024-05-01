from django.urls import include, path

from hottrack import views

urlpatterns = [path("", views.index)]
