from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from job.models import JobStatisticsLatest, JobStatistics
from job.serializers import DashboardSerializer, JobStatisticsSerializer
from oa_admin.customer.authentication import MyAuthentication, SimpleJWTAuthentication
from oa_admin.customer.pagination import SimpleLimitOffsetPagination


class JobStatisticsList(generics.ListAPIView):
    queryset = JobStatistics.objects.all()
    serializer_class = JobStatisticsSerializer
    authentication_classes = [SimpleJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = SimpleLimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job_id', 'dem_id', 'sup_id', 'statistics_time']


class Dashboard(generics.ListAPIView):
    serializer_class = DashboardSerializer
    queryset = JobStatisticsLatest.objects.all()
    authentication_classes = [SimpleJWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = SimpleLimitOffsetPagination

