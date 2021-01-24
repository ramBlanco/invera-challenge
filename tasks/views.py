from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tasks.models import Task
from tasks.serializers.tasksCreateSerializer import TasksCreateSerializer
from tasks.serializers.taskUpdateSerializer import TasksUpdateSerializer
from tasks.serializers.tasksListSerializer import TasksListSerializer
from tasks.serializers.taskUpdateStatusSerializer import TasksUpdateStatusSerializer
from rest_framework import generics

from datetime import datetime

class TaskList(generics.ListAPIView):
    """
    List all tasks, or create a new tasks.
    """

    def get(self, request, format=None):
        filters = {
            'title__icontains': request.query_params.get('search', ''),
            'created_at__lte': request.query_params.get('end_at', datetime.now())
        }
        if request.query_params.get("start_at") is not None:
            start_at_obj = datetime.strptime(request.query_params.get("start_at"), '%Y-%m-%d')
            filters['created_at__gte'] = datetime.combine(start_at_obj.date(), datetime.min.time()) 
            
        tasks = Task.objects.filter(**filters)
        serializer = TasksListSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TasksCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskStatus(generics.ListAPIView):
    """
    Update status task
    """
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TasksUpdateStatusSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(generics.ListAPIView):
    """
    Retrieve, update or delete a task
    """
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TasksListSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TasksUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)