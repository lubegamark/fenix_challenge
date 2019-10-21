from django.db import models


class MomoRequest(models.Model):
    PENDING = 'PENDING'
    SUCCESSFUL = 'SUCCESSFUL'
    FAILED = 'FAILED'
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (SUCCESSFUL, SUCCESSFUL),
        (FAILED, FAILED),
    )
    customer = models.CharField(max_length=250,)
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    status = models.CharField(
        max_length=250,
        choices=STATUS_CHOICES,
        default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Initialize a momo payment after saving
        """
        super().save(*args, **kwargs)
        make_momo_collection_request()


def make_momo_collection_request():
    pass
