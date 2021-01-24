from rest_framework import serializers
from tasks.models import Task


class TasksUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    completed = serializers.DateTimeField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Task` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance