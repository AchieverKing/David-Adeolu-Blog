from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import CommentForm
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views import View


# Create your views here.

class HomePageView(TemplateView):
    template_name = "blog/homepage.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().order_by("-date")[:3]
        return context

    


class PostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


class PosrArticleView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_later = post_id in stored_posts
        else:
            is_saved_later = False

        return is_saved_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags":post.tag.all(),
            "post_comment": CommentForm(),
            "comments": post.comment.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post_article.html", context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-article", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tag.all(),
            "post_comment": form,
            "comments": post.comment.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post_article.html", context)



class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) ==0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True 

        return render(request, "blog/stored_post.html", context)
        

    def post(self, request):
        stored_posts = request.session.get("stored_posts") 

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")