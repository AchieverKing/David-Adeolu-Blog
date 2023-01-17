from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name='homepage'),
    path("posts", views.PostsView.as_view(), name="posts"),
    path("posts/<slug:slug>", views.PosrArticleView.as_view(), name="post-article"),
    path("read_later", views.ReadLaterView.as_view(), name="read_later")
]

