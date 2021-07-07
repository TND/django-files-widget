from django.db import models
from topnotchdev import files_widget
from django.urls import reverse


class MyModel(models.Model):
    images = files_widget.ImagesField()

    def get_absolute_url(self):
        return reverse("demo-update", kwargs={'pk': self.pk})


class MyModelTwoFields(models.Model):
    avatar = files_widget.ImagesField()
    scene = files_widget.ImagesField()
    place = models.CharField(max_length=255, blank=False)

    def get_absolute_url(self):
        return reverse("demo2-update", kwargs={'pk': self.pk})
