from django.db import models
from uuid import uuid4
from django.db.models import QuerySet, Manager
from django.utils import timezone

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)


    class Meta:
        abstract = True


class SoftQuerySet(QuerySet):
    def delete(self):
        return self.update(is_deleted = True, deleted_at = timezone.now())      


class SoftManager(Manager):
    def get_queryset(self) -> QuerySet:
        return SoftQuerySet(self.model, self._db).filter(Q(is_deleted=False) | Q(is_deleted__isnull= True))


class SoftDeleteModel(models.Model):
    objects = SoftManager()

    is_deleted = models.BooleanField(null=True, blank=True, editable=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False, db_index=True)


    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        

    class Meta:
        abstract = True


class TimeStampMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)