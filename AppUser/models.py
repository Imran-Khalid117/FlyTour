from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.


class ApplicationUser(AbstractUser):
    """
    This class in inherited from AbstractUser class so that we can leverage already created fields in user model.

    Fields:
        created_at: DateTime field - do not need to set, it has default value
        updated_at: DateTime field - do not need to set, it has default value
        is_deleted: Boolean field - do not need to set, it has default value
    """
    # Add any additional fields you need for your user model
    refresh_token = models.CharField(max_length=500, blank=True, null=True)
    access_token = models.CharField(max_length=500, blank=True, null=True)
    access_token_expiry = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "db_application_user"
