from django.contrib import admin
from .models import FemrJob


@admin.register(FemrJob)
class FemrJobAdmin(admin.ModelAdmin):
    list_display = ['pk', 'group', 'status', 'started_at', 'finished_at', 'created_at']
    list_filter = ['group', 'status']
    readonly_fields = ['celery_task_id', 'log_file', 'output_prefix', 'started_at', 'finished_at', 'created_at']
