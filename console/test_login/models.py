from django.db import models


# Create your models here.
class LogModel(models.Model):
    started_time = models.DateTimeField()
    elapsed_time = models.FloatField(max_length=10)
    total_run_num = models.PositiveIntegerField()
    pass_case_num = models.PositiveIntegerField()
    failed_case_num = models.PositiveIntegerField()
    detail_log = models.TextField(blank=True)
    browser_type = models.CharField(max_length=10)

    class Meta:
        ordering = ['-started_time']

    def __str__(self):
        return "%s %s total=%d fail=%d" % \
               (self.started_time, self.browser_type, self.total_run_num, self.failed_case_num)

