from django.db import models


class JobStatistics(models.Model):
    statistics_time = models.DateTimeField(auto_now_add=True)
    job_id = models.CharField(max_length=64)
    dem_id = models.CharField(max_length=12)
    sup_id = models.CharField(max_length=12)
    avg_cost = models.IntegerField()
    sum_use = models.IntegerField()
    success_rate = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_statistics'


class JobLog(models.Model):
    job_id = models.CharField(max_length=64)
    dem_id = models.CharField(max_length=12)
    sup_id = models.CharField(max_length=12)
    code = models.CharField(max_length=12)
    msg = models.CharField(max_length=255)
    cost = models.IntegerField()
    request_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_log'


class JobStatisticsLatest(models.Model):
    statistics_time = models.DateTimeField(auto_now_add=True)
    job_id = models.CharField(max_length=64)
    dem_id = models.CharField(max_length=12)
    sup_id = models.CharField(max_length=12)
    avg_cost = models.IntegerField()
    sum_use = models.IntegerField()
    success_rate = models.IntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_statistics_latest'
