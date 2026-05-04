import os
from django.db import models
from django.core.files.base import ContentFile


class TransformJob(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_DONE, 'Done'),
        (STATUS_FAILED, 'Failed'),
    ]

    FORMAT_EXCEL = 'excel'
    FORMAT_CSV = 'csv'
    FORMAT_CHOICES = [
        (FORMAT_EXCEL, 'Excel (.xlsx)'),
        (FORMAT_CSV,   'CSV (.csv)'),
    ]

    input_file = models.FileField(upload_to='uploads/')
    output_file = models.FileField(upload_to='outputs/', blank=True)
    output_format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default=FORMAT_EXCEL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Job #{self.pk} — {self.get_status_display()}'

    # ── Lifecycle helpers ──────────────────────────────────────────────────────

    def mark_processing(self):
        self.status = self.STATUS_PROCESSING
        self.save(update_fields=['status', 'updated_at'])

    def complete(self, output_bytes: bytes):
        """Attach output file and mark job as done."""
        stem = os.path.splitext(os.path.basename(self.input_file.name))[0]
        ext = '.csv' if self.output_format == self.FORMAT_CSV else '.xlsx'
        output_name = f'output_{stem}{ext}'
        self.output_file.save(output_name, ContentFile(output_bytes), save=False)
        self.status = self.STATUS_DONE
        self.save(update_fields=['output_file', 'status', 'updated_at'])

    def fail(self, error: str):
        self.status = self.STATUS_FAILED
        self.error_message = error
        self.save(update_fields=['status', 'error_message', 'updated_at'])

    # ── Convenience properties ─────────────────────────────────────────────────

    @property
    def input_filename(self):
        return os.path.basename(self.input_file.name) if self.input_file else ''

    @property
    def output_filename(self):
        return os.path.basename(self.output_file.name) if self.output_file else ''

    @property
    def is_done(self):
        return self.status == self.STATUS_DONE

    @property
    def is_failed(self):
        return self.status == self.STATUS_FAILED
