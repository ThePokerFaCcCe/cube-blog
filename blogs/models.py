from django.db import models


class Category(models.Model):
    title = models.CharField("title", max_length=100)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    title = models.CharField("title", max_length=100, blank=False, null=False)
    description = models.TextField(
        "description", max_length=2500, blank=False, null=False
    )
    image = models.ImageField("image", null=True, blank=True)
    image_url = models.CharField("image_url", max_length=250, blank=False, null=False)
    create_date = models.DateTimeField(
        "create_date", auto_now_add=True, blank=False, null=False
    )

    category = models.ForeignKey(
        to=Category, on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    name = models.CharField("name", max_length=100, blank=False, null=False)
    email = models.EmailField("email", max_length=100, blank=False, null=False)
    website = models.CharField("website", max_length=100, blank=False, null=False)
    comment = models.TextField("comment", max_length=2500, blank=False, null=False)

    create_date = models.DateTimeField(
        "create_date", auto_now_add=True, blank=False, null=False
    )

    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self) -> str:
        return f"{self.comment[:20]}..." if len(self.comment) > 20 else self.comment
