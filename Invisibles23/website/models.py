from django.db import models

# Create your models here.
class WebpageSection (models.Model):
    name = models.CharField(max_length=50) # To reference the section in the template
    title = models.CharField(max_length=50) # Actual title of the section
    text = models.TextField(max_length=10000)
    custom_html = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title