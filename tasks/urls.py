from django.urls import path
from tasks import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.TaskList.as_view()),
    path('<int:pk>/', views.TaskDetail.as_view()),
    path('complete/<int:pk>/', views.TaskStatus.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)