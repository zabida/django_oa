from rest_framework import serializers

from job.models import JobStatisticsLatest


class DashboardSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobStatisticsLatest
        fields = '__all__'
