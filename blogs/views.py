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
        search_query = self.request.query_params.get("search")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
        return queryset

    @decorators.action(["get"], detail=False)
    def recent(self, request):
        recent_posts = self.get_queryset().order_by("-create_date")[:5]

        serializer = self.get_serializer(recent_posts, many=True)
        return response.Response(serializer.data)

    @decorators.action(["get"], detail=True, url_path="suggest")
    def sugget_next(self, request, pk=None):
        pk = int(pk)
        prev_post = self.get_queryset().filter(id=pk - 1).first()
        next_post = self.get_queryset().filter(id=pk + 1).first()

        prev_post_serializer = self.get_serializer(prev_post) if prev_post else None
        next_post_serializer = self.get_serializer(next_post) if next_post else None
        return response.Response(
            {
                "previous": prev_post_serializer.data if prev_post_serializer else None,
                "next": next_post_serializer.data if next_post_serializer else None,
            }
        )


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
