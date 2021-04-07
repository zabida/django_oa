from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from job import views

urlpatterns = [
    path('job_statistics/g/', views.JobStatisticsList.as_view()),
    path('dashboard/g/', views.Dashboard.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

