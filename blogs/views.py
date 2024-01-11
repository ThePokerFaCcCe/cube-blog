from . import serializers
from . import models
from rest_framework import viewsets, pagination, decorators, response


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Category instances.
    """

    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Post instances.
    """

    serializer_class = serializers.PostSerializer
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        queryset = models.Post.objects.all()
        category_id = self.request.query_params.get("category_id")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @decorators.action(["get"], detail=False)
    def recent(self, request):
        recent_posts = self.get_queryset().order_by("-create_date")[:5]

        serializer = self.get_serializer(recent_posts, many=True)
        return response.Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Comment instances.
    """

    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        queryset = models.Comment.objects.all()
        post_id = self.request.query_params.get("post_id")
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        return queryset

    @decorators.action(["get"], detail=False)
    def recent(self, request):
        recent_comments = self.get_queryset().order_by("-create_date")[:5]

        serializer = self.get_serializer(recent_comments, many=True)
        return response.Response(serializer.data)
