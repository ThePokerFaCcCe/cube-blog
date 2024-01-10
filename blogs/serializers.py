from rest_framework import serializers

from . import models


class PostSerializer(serializers.ModelSerializer):
    creator = UserInfoSerializer(read_only=True)
    user: UserInfoSerializer = serializers.SerializerMethodField()

    class Meta:
        model = models.Post
        fields = [
            "title",
            "description",
            "image",
            "create_date",
            "category",
        ]

    # def get_user(self, pv: PrivateChat):
    #     if (request := self.context.get('request')):
    #         self_user = request.user
    #         if (another := pv.get_reciever_user(self_user)):
    #             return UserInfoSerializer(another).data
