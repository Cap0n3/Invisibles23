from django.db import models
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from datetime import date

# == Base models to stay DRY == #
class BaseThematic(models.Model):
    """
    Base class for the thematic models
    """
    order = models.PositiveIntegerField(
        default=None,
        verbose_name=f"Ordre de la section",
        blank=True,
        null=True,
        help_text="Laisser vide pour ajouter la section à la fin ou mettre 0 pour ne pas afficher la section"
    )
    title = models.CharField(max_length=100, verbose_name="Titre de la section")
    richText = RichTextField(verbose_name="Contenu de la section")
    custom_html = models.TextField(blank=True)
    image = models.ImageField(upload_to='', blank=True, verbose_name="Image de la section")
    image_title = models.CharField(max_length=50, blank=True, verbose_name="Titre de l'image")
    image_alt = models.CharField(max_length=50, blank=True, verbose_name="Texte alternatif de l'image")
    reverse = models.BooleanField(default=False, verbose_name="Inverser l'ordre de l'image et du texte")

    class Meta:
        abstract = True

    def __str__(self):
        return mark_safe(f"<span style='color: #BC52BE'>[ORDRE SECTION : {self.order}] {'<i>(section non visible)</i>' if self.order == 0 else ''}</span> - {self.title} ")

    def clean(self):
        super().clean()
        # Check if another section with the same tab and order already exists
        existing_sections = self.__class__.objects.filter(order=self.order).exclude(pk=self.pk)
        if existing_sections.exists() and self.order != 0:
            raise ValidationError(mark_safe(f"""
                <p>Une section avec le même ordre existe déjà dans cet onglet !
                Veuillez changer l'ordre de la section ou l'onglet associé.</p>
                <p>Si vous souhaitez échanger l'ordre de deux sections :</p>
                <ol>
                    <li>1. Mettez l'ordre de la section que vous souhaitez échanger à 0</li>
                    <li>2. Enregistrez</li>
                    <li>3. Mettez l'ordre de l'autre section avec laquelle vous souhaitez échanger à l'ordre de la première section</li>
                    <li>4. Enregistrez</li>
                    <li>5. Mettez l'ordre de la première section à l'ordre de la deuxième section</li>
                </ol>
            """))


    def save(self, *args, **kwargs):
        # If the order is None, set the order to the total number of sections + 1
        if self.order is None:
            self.order = self.get_total_sections() + 1

        super().save(*args, **kwargs)

    def get_total_sections(self):
        return self.__class__.objects.count()

class BaseRessources(models.Model):
    """
    Base class for the ressources models
    """
    title = models.CharField(max_length=100, verbose_name="Titre de la section")
    description = models.TextField(max_length=500, verbose_name="Description de la ressource (max 500 caractères)")
    address = models.CharField(max_length=100, blank=True, verbose_name="Adresse de la ressource")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone de la ressource")
    link = models.URLField(verbose_name="Lien vers la ressource", blank=True)
    image = models.ImageField(upload_to='', default="DefaultRessources.jpg" ,blank=True, verbose_name="Image de la section")
    image_title = models.CharField(max_length=50, blank=True, default="Default image", verbose_name="Titre de l'image")
    image_alt = models.CharField(max_length=50, blank=True, default="Default image", verbose_name="Texte alternatif de l'image")
    keywords = models.CharField(max_length=100, verbose_name="Mots-clés (séparés par des virgules)")

class AdminRessources(BaseRessources):
    class Meta:
        verbose_name = "Ressources administratives"
        verbose_name_plural = "Ressources administratives"

    def __str__(self):
        return self.title
    
class TherapeuticRessources(BaseRessources):
    class Meta:
        verbose_name = "Ressources thérapeutiques"
        verbose_name_plural = "Ressources thérapeutiques"

    def __str__(self):
        return self.title

class FinancialRessources(BaseRessources):
    class Meta:
        verbose_name = "Ressources financières"
        verbose_name_plural = "Ressources financières"

    def __str__(self):
        return self.title

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

class ChronicTabSections(BaseThematic):
    class Meta:
        # Order the sections by the order field in the admin
        ordering = ['order']
        # Change visible name of the model in the admin
        verbose_name = 'Maladies chroniques'
        verbose_name_plural = 'Maladies chroniques'

class InvsibleTabSections(BaseThematic):
    class Meta:
        # Order the sections by the order field in the admin
        ordering = ['order']
        # Change visible name of the model in the admin
        verbose_name = 'Maladies invisibles'
        verbose_name_plural = 'Maladies invisibles'

class MiscarriageTabSections(BaseThematic):
    class Meta:
        # Order the sections by the order field in the admin
        ordering = ['order']
        # Change visible name of the model in the admin
        verbose_name = 'Fausses couches'
        verbose_name_plural = 'Fausses couches'

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

class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Titre de l'évènement")
    short_description = models.TextField(max_length=300, verbose_name="Description courte de l'évènement (max 300 caractères)")
    full_description = RichTextField(verbose_name="Description complète de l'évènement")
    date = models.DateField(verbose_name="Date de l'évènement")
    start_time = models.TimeField(verbose_name="Heure de début de l'évènement", default="00:00")
    end_time = models.TimeField(verbose_name="Heure de fin de l'évènement", default="01:00")
    address = models.CharField(max_length=100, blank=True, verbose_name="Adresse de l'évènement")
    link = models.URLField(blank=True)

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"
        ordering = ['-date']

    def clean(self):
        '''
        Check if the event is not in the past
        '''
        super().clean()
        if self.date < date.today():
            raise ValidationError("La date de l'évènement ne peut pas être dans le passé !")
        
        # Check if start time is before end time
        if self.start_time > self.end_time:
            raise ValidationError("L'heure de début de l'évènement doit être avant l'heure de fin !")
        
        # Check if the event is not too long
        if self.end_time.hour - self.start_time.hour > 24:
            raise ValidationError("L'évènement ne peut pas durer plus de 24 heures !")
    
    def __str__(self):
        return self.title + " - " + str(self.date)