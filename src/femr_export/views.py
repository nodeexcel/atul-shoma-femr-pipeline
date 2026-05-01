import json
import logging
import mimetypes
import os
from pathlib import Path

from django.contrib import messages
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import FemrJob
from .tasks import run_femr_export

logger = logging.getLogger('femr_export.views')

GROUPS = ['WFD', 'Internal', 'Comml', 'OGA', 'ADP', 'All']


def index(request):
    recent_jobs = FemrJob.objects.all()[:20]
    return render(request, 'femr_export/index.html', {
        'groups': GROUPS,
        'recent_jobs': recent_jobs,
    })


@require_POST
def run_job(request):
    group = request.POST.get('group', '').strip()
    if group not in GROUPS:
        messages.error(request, 'Invalid group selected.')
        return redirect('femr_export:index')

    # Check if a job for this group (or All) is already active
    if group == 'All':
        active = FemrJob.objects.filter(status__in=['pending', 'running']).first()
    else:
        active = FemrJob.objects.filter(
            group__in=[group, 'All'],
            status__in=['pending', 'running'],
        ).first()

    if active:
        messages.warning(
            request,
            f'A job for <strong>{active.group}</strong> is already running '
            f'(Job #{active.pk}). '
            f'<a href="/femr/jobs/{active.pk}/" class="alert-link">View it here.</a>',
        )
        return redirect('femr_export:index')

    from django.conf import settings
    log_dir = settings.FEMR_JOB_LOG_DIR

    job = FemrJob.objects.create(group=group)
    job.log_file = str(Path(log_dir) / f'job_{job.pk}.log')
    job.save(update_fields=['log_file'])

    run_femr_export.delay(job.pk)
    logger.info("Dispatched job #%s for group %s", job.pk, group)

    return redirect('femr_export:job_detail', pk=job.pk)


def job_detail(request, pk):
    job = get_object_or_404(FemrJob, pk=pk)
    return render(request, 'femr_export/job_detail.html', {'job': job})


def log_poll(request, pk):
    """Return new log lines since byte offset. Used by JS polling."""
    job = get_object_or_404(FemrJob, pk=pk)

    try:
        offset = int(request.GET.get('offset', 0))
    except (TypeError, ValueError):
        offset = 0

    lines = ''
    new_offset = offset

    if job.log_file and os.path.exists(job.log_file):
        with open(job.log_file, 'r', errors='replace') as f:
            f.seek(offset)
            chunk = f.read()
            lines = chunk
            new_offset = offset + len(chunk.encode('utf-8', errors='replace'))

    return JsonResponse({
        'lines': lines,
        'offset': new_offset,
        'done': not job.is_active,
        'status': job.status,
    })


def download_file(request, pk, filename):
    job = get_object_or_404(FemrJob, pk=pk)

    if not job.is_done:
        raise Http404('Job not complete.')

    # Verify the filename belongs to this job's output files
    output_files = dict(job.output_files)  # {filename: path}
    if filename not in output_files:
        raise Http404('File not found.')

    file_path = output_files[filename]
    content_type, _ = mimetypes.guess_type(filename)
    content_type = content_type or 'application/octet-stream'

    logger.info("Job #%s: downloading %s", pk, filename)
    return FileResponse(
        open(file_path, 'rb'),
        content_type=content_type,
        as_attachment=True,
        filename=filename,
    )
