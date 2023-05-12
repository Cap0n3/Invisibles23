from django.db import models

# Create your models here.
class WebpageSection (models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title