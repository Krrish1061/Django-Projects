from rest_framework import fields, serializers
from blogpost.models import Post
from userprofile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()

    class Meta:
        model = Post
        fields = '__all__'
