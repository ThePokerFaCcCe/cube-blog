from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = [
            "id",
            "title",
        ]


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(
        queryset=models.Post.objects.all(),
        required=True,
        allow_null=False,
        write_only=True,
    )

    class Meta:
        model = models.Comment
        fields = [
            "id",
            "name",
            "email",
            "website",
            "comment",
            "post",
            "post_id",
        ]
        extra={"post_id":{'read_only':True}}


class PostSerializer(serializers.ModelSerializer):
    categoryName = (
        serializers.SerializerMethodField()
    )  # CategorySerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all(),
        required=True,
        allow_null=False,
        write_only=True,
    )
    # user: UserInfoSerializer = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = [
            "id",
            "title",
            "description",
            # "image",
            "image_url",
            "create_date",
            "categoryName",
            "category",
            "comments",
        ]

    # def get_user(self, pv: PrivateChat):
    #     if (request := self.context.get('request')):
    #         self_user = request.user
    #         if (another := pv.get_reciever_user(self_user)):
    #             return UserInfoSerializer(another).data

    def get_categoryName(self, post):
        return post.category.title
