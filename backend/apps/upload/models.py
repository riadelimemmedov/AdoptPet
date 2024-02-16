from django.db import models


# Create your models here.
class Upload(models.Model):
    upload_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
