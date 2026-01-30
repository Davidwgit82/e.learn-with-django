from django.db import models
from django.utils.text import slugify

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True 

class SlugBaseModel(models.Model):
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        abstract = True 

    def save(self, *args, **kwargs):
        if not self.slug:
            value = getattr(self, 'title', getattr(self, 'name', None))
            if value: 
                self.slug = slugify(value)
        super().save(*args, **kwargs)