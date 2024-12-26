from django.db import models


class File(models.Model):
    link = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    hash = models.CharField(max_length=100)

    def __str__(self):
        return self.link
