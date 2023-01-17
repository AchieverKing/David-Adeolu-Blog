from django.db import models
from django.urls import reverse

# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name_plural = "Tags"



class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images")
    date = models.DateField(auto_now=True)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True, unique=True)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, related_name="post")
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("details", args=[self.slug])


class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")

