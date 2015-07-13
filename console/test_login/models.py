from django.db import models


# Create your models here.
class LogModel(models.Model):
    started_time = models.DateTimeField()
    elapsed_time = models.CharField(max_length=10)
    total_run_num = models.PositiveIntegerField()
    pass_case_num = models.PositiveIntegerField()
    failed_case_num = models.PositiveIntegerField()
    detail_log = models.TextField(blank=True)
    browser_type = models.CharField(max_length=10)

    class Meta:
        ordering = ['-started_time']
    def __str__(self):
        return "%s:%s" % ('aaa', self.detail_log)

