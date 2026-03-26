from django.contrib import admin
from .models import TransformJob


@admin.register(TransformJob)
class TransformJobAdmin(admin.ModelAdmin):
    list_display = ('pk', 'input_filename', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    readonly_fields = ('input_file', 'output_file', 'status', 'error_message', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    def input_filename(self, obj):
        return obj.input_filename
    input_filename.short_description = 'Input File'
