from django.db import models
from Dashboard.help import snd_email

#this is the Moddel form here that would be responsible for how we would be uploading tutorial videos
class Tutorial(models.Model):

    title = models.CharField( max_length=50)
    video_url = models.URLField( max_length=200)

    class Meta:
        verbose_name = ("Tutorial")
        verbose_name_plural = ("Tutorials")

    def __str__(self):
        return self.title

 
#? For support notification from the help section
class Support_Message (models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    school = models.ForeignKey("Dashboard.School", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def send_notification (self, template, send_to):
        snd_email(self.title, template, send_to)