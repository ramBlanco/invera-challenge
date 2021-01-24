from rest_framework import serializers
from tasks.models import Task


class TasksListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed','created_at']
