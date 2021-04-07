from rest_framework import serializers

from job.models import JobStatisticsLatest, JobStatistics


class JobStatisticsSerializer(serializers.ModelSerializer):
    statistics_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = JobStatistics
        fields = '__all__'


class DashboardSerializer(serializers.ModelSerializer):
    statistics_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = JobStatisticsLatest
        fields = '__all__'

