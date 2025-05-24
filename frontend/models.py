from django.db import models
from django.conf import settings


class Photo(models.Model):
    image = models.ImageField(verbose_name='image')
    caption = models.CharField(max_length=128, blank=True, verbose_name='légende')
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
