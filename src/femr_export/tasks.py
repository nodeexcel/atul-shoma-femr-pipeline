import logging
import subprocess
import sys
from pathlib import Path

from celery import shared_task
from django.conf import settings

logger = logging.getLogger('femr_export.tasks')


@shared_task(bind=True)
def run_femr_export(self, job_id: int):
    from .models import FemrJob

    job = FemrJob.objects.get(pk=job_id)
    job.mark_running(celery_task_id=self.request.id)

    log_path = Path(job.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    output_dir = settings.FEMR_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)

    # Output prefix: femr_v15_wfd, femr_v15_adp, etc. (or femr_v15 for All)
    group_slug = job.group.lower() if job.group != 'All' else ''
    prefix_name = f'femr_v15_{group_slug}' if group_slug else 'femr_v15'
    output_prefix = str(output_dir / prefix_name)

    job.output_prefix = prefix_name
    job.save(update_fields=['output_prefix'])

    # Use the container/env Python — not the dev venv path
    python = getattr(settings, 'FEMR_PYTHON', sys.executable)
    script = str(settings.FEMR_SCRIPT)
    repo_root = str(settings.FEMR_REPO_ROOT)

    cmd = [python, '-u', script, '-o', output_prefix, '--workers', '40']
    if job.group != 'All':
        cmd += ['--group', job.group]

    logger.info("Job #%s: starting — group=%s cmd=%s", job_id, job.group, ' '.join(cmd))

    try:
        with open(log_path, 'w', buffering=1) as log_fh:
            proc = subprocess.Popen(
                cmd,
                stdout=log_fh,
                stderr=subprocess.STDOUT,
                cwd=repo_root,
                text=True,
            )
            proc.wait()

        if proc.returncode == 0:
            job.complete()
            logger.info("Job #%s: completed successfully", job_id)
        else:
            job.fail(f'Script exited with code {proc.returncode}')
            logger.error("Job #%s: script exited with code %s", job_id, proc.returncode)

    except Exception as exc:
        logger.exception("Job #%s: unexpected error", job_id)
        job.fail(str(exc))
