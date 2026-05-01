import glob
from django.conf import settings
from django.db import models
from django.utils import timezone


class FemrJob(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_RUNNING = 'running'
    STATUS_DONE    = 'done'
    STATUS_FAILED  = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_RUNNING, 'Running'),
        (STATUS_DONE,    'Done'),
        (STATUS_FAILED,  'Failed'),
    ]

    GROUP_CHOICES = [
        ('WFD',      'WFD'),
        ('Internal', 'Internal'),
        ('Comml',    'Comml'),
        ('OGA',      'OGA'),
        ('ADP',      'ADP'),
        ('All',      'All Groups'),
    ]

    group          = models.CharField(max_length=20, choices=GROUP_CHOICES)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    celery_task_id = models.CharField(max_length=255, blank=True)
    log_file       = models.CharField(max_length=500, blank=True)
    output_prefix  = models.CharField(max_length=500, blank=True)
    started_at     = models.DateTimeField(null=True, blank=True)
    finished_at    = models.DateTimeField(null=True, blank=True)
    error_message  = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Job #{self.pk} — {self.group} — {self.get_status_display()}'

    # ── Lifecycle helpers ──────────────────────────────────────────────────────

    def mark_running(self, celery_task_id=''):
        self.status = self.STATUS_RUNNING
        self.celery_task_id = celery_task_id
        self.started_at = timezone.now()
        self.save(update_fields=['status', 'celery_task_id', 'started_at'])

    def complete(self):
        self.status = self.STATUS_DONE
        self.finished_at = timezone.now()
        self.save(update_fields=['status', 'finished_at'])

    def fail(self, error: str):
        self.status = self.STATUS_FAILED
        self.error_message = error
        self.finished_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'finished_at'])

    # ── Convenience properties ─────────────────────────────────────────────────

    @property
    def is_active(self):
        return self.status in (self.STATUS_PENDING, self.STATUS_RUNNING)

    @property
    def is_done(self):
        return self.status == self.STATUS_DONE

    @property
    def is_failed(self):
        return self.status == self.STATUS_FAILED

    @property
    def output_files(self):
        """Return list of (filename, absolute_path) for all generated xlsx files."""
        if not self.output_prefix:
            return []
        pattern = str(settings.FEMR_OUTPUT_DIR / f'{self.output_prefix}*.xlsx')
        paths = sorted(glob.glob(pattern))
        return [(p.split('/')[-1], p) for p in paths]

    @property
    def duration(self):
        if self.started_at and self.finished_at:
            delta = self.finished_at - self.started_at
            mins, secs = divmod(int(delta.total_seconds()), 60)
            hours, mins = divmod(mins, 60)
            if hours:
                return f'{hours}h {mins}m {secs}s'
            return f'{mins}m {secs}s'
        return None
