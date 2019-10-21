from celery.task.schedules import crontab
from celery.decorators import periodic_task
from momo_integration import models


# Run every 5 minutes
@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="poll_pending_requests",
    ignore_result=True)
def poll_pending_requests():
    """Check status of all pending requests

    Query all pending requests, and poll each one
    Default time is every 5 minutes
    """
    pending_transactions = models.MomoRequest.objects.filter(
        status=models.MomoRequest.PENDING)

    for momo_request in pending_transactions:
        models.poll_transaction(momo_request.id)
