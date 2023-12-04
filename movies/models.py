from django.db import models
from users.models import User
import uuid

class CollectionTitle(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=255, blank=False, null=False)
  description = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title
  


class MovieCollection(models.Model):
    collection_id = models.ForeignKey(CollectionTitle, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    genres = models.CharField(max_length=255, blank=False, null=False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return self.title