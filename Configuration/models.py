from django.db import models

# Create your models here.

#this is the Moddel form here that would be responsible for how we would be uploading tutorial videos
class Tutorial(models.Model):

    title = models.CharField( max_length=50)
    video_url = models.URLField( max_length=200)

    class Meta:
        verbose_name = ("Tutorial")
        verbose_name_plural = ("Tutorials")

    def __str__(self):
        return self.title

 
