from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser

class Meta:
        app_label = 'mys'

class CustomUser(AbstractUser):
    pass
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mode = models.CharField(max_length=20, default='all')

# Create your models here.
class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"