from rest_framework import serializers
from rest_framework.authtoken.admin import User

from .models import *

from rest_framework import serializers
from .models import  StudyPlan

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PlanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudyPlan
        fields = '__all__'


