from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField

# Models for the website
class HomePageSections (models.Model):
    name = models.CharField(max_length=50) # To reference the section in the template
    title = models.CharField(max_length=50) # Actual title of the section
    text = models.TextField(max_length=10000)
    custom_html = models.TextField(blank=True)
    image = models.ImageField(upload_to='')
    image_title = models.CharField(max_length=50, blank=True)
    image_alt = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title
    
class AboutPageSections(HomePageSections):
    pass

class AssociationSections(HomePageSections):
    pass

class ThematicSections(models.Model):
    ASSOCIATED_TAB = [('chronic', 'Maladies chroniques'), ('invisible', 'Maladies invisibles'), ('miscarriage', 'Fausses couches')]
    tab = models.CharField(max_length=20, choices=ASSOCIATED_TAB, default='chronic', verbose_name="Onglet associé")
    title = models.CharField(max_length=100, verbose_name="Titre de la section")
    richText = RichTextField(verbose_name="Contenu de la section")
    custom_html = models.TextField(blank=True)
    image = models.ImageField(upload_to='', blank=True, verbose_name="Image de la section")
    image_title = models.CharField(max_length=50, blank=True, verbose_name="Titre de l'image")
    image_alt = models.CharField(max_length=50, blank=True, verbose_name="Texte alternatif de l'image")
    reverse = models.BooleanField(default=False, verbose_name="Inverser l'ordre de l'image et du texte")

    def __str__(self):
        return self.title



class YoutubeVideos(models.Model):
    title = models.CharField(max_length=50)
    video_url = models.URLField()

    def clean(self):
        '''
        Clean the video_url field to get the embed link
        '''
        super().clean()
        try:
            if "youtu.be" in self.video_url:
                vidID = self.video_url.split("/")[-1]  # Get last bit where ID is
                self.video_url = f"https://www.youtube.com/embed/{vidID}"
            elif "youtube.com" in self.video_url:
                vidID = self.video_url.split("=")[-1]
                self.video_url = f"https://www.youtube.com/embed/{vidID}"
            else:
                raise ValidationError("Le lien de la vidéo youtube est invalide !")
        except Exception as e:
            self.video_url = ""
            raise ValidationError(f"Error: {str(e)}")
        
        total_videos = YoutubeVideos.objects.count()
        
        if total_videos >= 5:
            raise ValidationError("Vous ne pouvez pas ajouter plus de 6 vidéos !")
    
    def __str__(self):
        return self.title
