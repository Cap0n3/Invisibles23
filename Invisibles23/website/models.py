from django.db import models

# Create your models here.
class WebpageSection (models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    
class Paragraphs (models.Model):
    section = models.ForeignKey(WebpageSection, on_delete=models.CASCADE)
    paragraph = models.TextField()

    def __str__(self):
        return self.paragraph