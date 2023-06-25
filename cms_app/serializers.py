from rest_framework.serializers import ModelSerializer,SerializerMethodField
from rest_framework import serializers
from .models import User, Post, Like


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password','username', 'gender','bio','profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_picture': {'required': False}
        }

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['name', 'username','gender', 'bio']


class PostSerializer(ModelSerializer):
    num_likes = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'owner', 'is_public','image','created_at','num_likes']

    def get_num_likes(self, obj):
        return obj.likes.count()


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'