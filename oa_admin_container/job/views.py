from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from job.models import JobStatisticsLatest
from job.serializers import DashboardSerializer
from oa_admin.customer.authentication import MyAuthentication, SimpleJWTAuthentication


class JobStatisticsList(generics.ListCreateAPIView):
    pass


class Dashboard(generics.ListAPIView):
    serializer_class = DashboardSerializer
    queryset = JobStatisticsLatest.objects.all()
    authentication_classes = [SimpleJWTAuthentication]
    permission_classes = [IsAuthenticated]
