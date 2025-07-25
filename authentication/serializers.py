from django.contrib.auth.models import Group, User
from rest_framework import serializers
from django.contrib.auth import get_user_model

# User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        # fields = ['url', 'username', 'email', 'groups']
        fields = ['username', 'email', 'password']



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
