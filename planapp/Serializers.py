from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import User, Plan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Plan
        fields = ['id', 'name', 'description', 'is_completed', 'deadline', 'archived', 'user']


