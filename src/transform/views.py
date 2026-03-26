import logging
import mimetypes

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, FormView

from .forms import UploadForm
from .models import TransformJob
from .services import run_transform

logger = logging.getLogger('transform.views')


class UploadView(FormView):
    template_name = 'transform/upload.html'
    form_class = UploadForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['recent_jobs'] = TransformJob.objects.all()[:10]
        return ctx

    def form_valid(self, form):
        job = TransformJob.objects.create(input_file=form.cleaned_data['input_file'])
        logger.info("Job #%s created for file: %s", job.pk, job.input_filename)

        try:
            job.mark_processing()
            output_bytes = run_transform(job.input_file.path)
            job.complete(output_bytes)
            logger.info("Job #%s completed successfully", job.pk)
        except Exception as exc:
            logger.error("Job #%s failed: %s", job.pk, exc, exc_info=True)
            job.fail(str(exc))

        return redirect('transform:job_detail', pk=job.pk)


class JobDetailView(DetailView):
    model = TransformJob
    template_name = 'transform/job_detail.html'
    context_object_name = 'job'


def download_output(request, pk):
    """Stream the output file to the browser as a download."""
    job = get_object_or_404(TransformJob, pk=pk)

    if not job.is_done or not job.output_file:
        raise Http404('Output file not available.')

    content_type, _ = mimetypes.guess_type(job.output_filename)
    content_type = content_type or 'application/octet-stream'

    response = FileResponse(
        job.output_file.open('rb'),
        content_type=content_type,
        as_attachment=True,
        filename=job.output_filename,
    )
    logger.info("Job #%s output downloaded: %s", job.pk, job.output_filename)
    return response
