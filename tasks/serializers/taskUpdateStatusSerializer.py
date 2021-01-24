from rest_framework import serializers
from tasks.models import Task
import datetime

class TasksUpdateStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    completed = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        """
        Update completed field and return an existing `Task` instance, given the validated data.
        """
        instance.completed = datetime.datetime.now()
        instance.save()
        return instance
