from django.db import models
from uuid import uuid4
from datetime import datetime


class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)

    
    class Meta:
        abstract = True


class TimeStampMixin:
    created_at = models.DateTimeField(auto_now_add=True, default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True, default=datetime.now)