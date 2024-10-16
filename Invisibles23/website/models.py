from django.db import models
from django.conf import settings
from Invisibles23.logging_config import logger
from Invisibles23.logging_utils import log_debug_info
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from django.utils.safestring import mark_safe
from datetime import date
from cloudinary.models import CloudinaryField

# == Base models to stay DRY == #
class BaseSections(models.Model):
    """
    Base class for the website standard sections models
    """

    name_ID = models.CharField(
        max_length=50
    )  # To reference the section in the template
    title = models.CharField(max_length=50)  # Actual title of the section
    richText = RichTextField(
        max_length=10000, default="Écrire ici", verbose_name="Contenu de la section"
    )
    custom_html = models.TextField(blank=True)
    image = CloudinaryField("image", blank=True)
    image_title = models.CharField(max_length=50, blank=True)
    image_alt = models.CharField(max_length=50, blank=True)
    reverse = models.BooleanField(
        default=False, verbose_name="Inverser l'ordre de l'image et du texte"
    )

    class Meta:
        abstract = True


class BaseThematic(models.Model):
    """
    Base class for the thematic models
    """

    order = models.PositiveIntegerField(
        default=None,
        verbose_name=f"Ordre de la section",
        blank=True,
        null=True,
        help_text="Laisser vide pour ajouter la section à la fin ou mettre 0 pour ne pas afficher la section",
    )
    title = models.CharField(max_length=100, verbose_name="Titre de la section")
    richText = RichTextField(verbose_name="Contenu de la section")
    custom_html = models.TextField(blank=True)
    image = CloudinaryField("image", blank=True)
    image_title = models.CharField(
        max_length=50, blank=True, verbose_name="Titre de l'image"
    )
    image_alt = models.CharField(
        max_length=50, blank=True, verbose_name="Texte alternatif de l'image"
    )
    reverse = models.BooleanField(
        default=False, verbose_name="Inverser l'ordre de l'image et du texte"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return mark_safe(
            f"<span style='color: #BC52BE'>[ORDRE SECTION : {self.order}] {'<i>(section non visible)</i>' if self.order == 0 else ''}</span> - {self.title} "
        )

    def clean(self):
        super().clean()
        # Check if another section with the same tab and order already exists
        existing_sections = self.__class__.objects.filter(order=self.order).exclude(
            pk=self.pk
        )
        if existing_sections.exists() and self.order != 0:
            raise ValidationError(
                mark_safe(
                    f"""
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
            """
                )
            )

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
    description = models.TextField(
        max_length=500, verbose_name="Description de la ressource (max 500 caractères)"
    )
    address = models.CharField(
        max_length=100, blank=True, verbose_name="Adresse de la ressource"
    )
    phone = models.CharField(
        max_length=20, blank=True, verbose_name="Numéro de téléphone de la ressource"
    )
    link = models.URLField(verbose_name="Lien vers la ressource", blank=True)
    image = CloudinaryField("image", blank=True)
    image_title = models.CharField(
        max_length=50,
        blank=True,
        default="Default image",
        verbose_name="Titre de l'image",
    )
    image_alt = models.CharField(
        max_length=50,
        blank=True,
        default="Default image",
        verbose_name="Texte alternatif de l'image",
    )
    keywords = models.CharField(
        max_length=100, verbose_name="Mots-clés (séparés par des virgules)"
    )

    # If image is not provided, use the default image
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = "default_Img_ressources"
        super().save(*args, **kwargs)


class AdminRessources(BaseRessources):
    class Meta:
        verbose_name = "Page Ressources - Administratives"
        verbose_name_plural = "Page Ressources - Administratives"

    def __str__(self):
        return self.title


class TherapeuticRessources(BaseRessources):
    class Meta:
        verbose_name = "Page Ressources - Thérapeutiques"
        verbose_name_plural = "Page Ressources - Thérapeutiques"

    def __str__(self):
        return self.title


class LibraryRessources(BaseRessources):
    class Meta:
        verbose_name = "Page Ressources - Bibliothèque"
        verbose_name_plural = "Page Ressources - Bibliothèque"

    def __str__(self):
        return self.title


# == Models for the website == #
class HomeSections(BaseSections):
    """
    Home page sections model
    """
    class Meta:
        verbose_name = "Page d'accueil"
        verbose_name_plural = "Page d'accueil"

    def __str__(self):
        return self.title


class AboutSections(BaseSections):
    """
    About page sections model
    """
    class Meta:
        verbose_name = "Page à propos"
        verbose_name_plural = "Page à propos"

    def __str__(self):
        return self.title


class AssoSections(BaseSections):
    """
    Association page sections model
    """
    class Meta:
        verbose_name = "Page association"
        verbose_name_plural = "Page association"

    def __str__(self):
        return self.title


class ChronicTabSections(BaseThematic):
    """
    Chronic diseases tab sections model
    """
    class Meta:
        # Order the sections by the order field in the admin
        ordering = ["order"]
        # Change visible name of the model in the admin
        verbose_name = "Page Thématiques - Maladies chroniques"
        verbose_name_plural = "Page Thématiques - Maladies chroniques"


class InvsibleTabSections(BaseThematic):
    """
    Invisible diseases tab sections model
    """
    class Meta:
        # Order the sections by the order field in the admin
        ordering = ["order"]
        # Change visible name of the model in the admin
        verbose_name = "Page Thématiques - Maladies invisibles"
        verbose_name_plural = "Page Thématiques - Maladies invisibles"


class MiscarriageTabSections(BaseThematic):
    """
    Not used in the website, but can be used to add a new tab for the miscarriage section
    """
    class Meta:
        # Order the sections by the order field in the admin
        ordering = ["order"]
        # Change visible name of the model in the admin
        verbose_name = "Fausses couches"
        verbose_name_plural = "Fausses couches"


class YoutubeVideos(models.Model):
    """
    Store the youtube videos to display them on the website
    """
    title = models.CharField(max_length=50)
    video_url = models.URLField()

    def clean(self):
        """
        Clean the video_url field to get the embed link
        """
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
    """
    Event model to manage the events on the website (e.g. talk event OR standard event)
    """

    is_talk_event = models.BooleanField(default=False, verbose_name="Groupe de parole")
    title = models.CharField(
        max_length=100,
        verbose_name="Titre de l'évènement",
        blank=False,
        default="Titre de l'évènement",
    )
    short_description = models.TextField(
        max_length=300,
        verbose_name="Description courte de l'évènement (max 300 caractères)",
        blank=False,
        default="Description courte de l'évènement",
    )
    full_description = RichTextField(
        verbose_name="Description complète de l'évènement",
        blank=False,
        default="Description complète de l'évènement",
    )
    date = models.DateField(verbose_name="Date de l'évènement", blank=False)
    start_time = models.TimeField(
        verbose_name="Heure de début de l'évènement", default="00:00", blank=False
    )
    end_time = models.TimeField(
        verbose_name="Heure de fin de l'évènement", default="01:00", blank=False
    )
    address = models.CharField(
        max_length=100, blank=True, verbose_name="Adresse de l'évènement"
    )
    link = models.URLField(blank=True, verbose_name="Lien de l'événement (optionnel)") # Optional link to the event
    talk_event_link = models.URLField(blank=True, verbose_name="Lien de réunion Zoom")
    participants_limit = models.PositiveIntegerField(
        default=9, verbose_name="Nombre maximum de participants (groupe de parole)"
    )
    is_fully_booked = models.BooleanField(
        default=False, verbose_name="Évènement complet"
    )
    participants = models.ManyToManyField(
        "Participant",
        through="EventParticipants",
        related_name="events",
        verbose_name="Participants",
    )

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"

    def clean(self):
        """
        Necessary validations for the event data (clean method is only called in the admin console or with ModelForm)
        """
        log_debug_info("Cleaning event data:", self, inspect_attributes=True)

        # Check if mandatory fields are filled
        if not self.title:
            raise ValidationError("Le titre de l'évènement est obligatoire !")
        
        if not self.short_description:
            raise ValidationError(
                "La description courte de l'évènement est obligatoire !"
            )
        
        if not self.full_description:
            raise ValidationError(
                "La description complète de l'évènement est obligatoire !"
            )
        
        if not self.date:
            raise ValidationError("Veuillez renseigner la date de l'évènement !")
        
        if not self.start_time:
            raise ValidationError(
                "Veuillez renseigner l'heure de début de l'évènement !"
            )
        if not self.end_time:
            raise ValidationError("Veuillez renseigner l'heure de fin de l'évènement !")

        if self.date < date.today():
            raise ValidationError(
                "La date de l'évènement ne peut pas être dans le passé !"
            )

        # Check if start time is before end time
        if self.start_time > self.end_time:
            raise ValidationError(
                "L'heure de début de l'évènement doit être avant l'heure de fin !"
            )

        # Check if the event is not too long
        if self.end_time.hour - self.start_time.hour > 24:
            raise ValidationError("L'évènement ne peut pas durer plus de 24 heures !")

        # Check if the participants limit is not too high
        if self.participants_limit > 50:
            raise ValidationError(
                "Le nombre maximum de participants ne peut pas être supérieur à 50 !"
            )

        # Check if the participants limit is not too low
        if self.participants_limit < 1:
            raise ValidationError(
                "Le nombre maximum de participants ne peut pas être inférieur à 1 !"
            )

        # Check if the participants limit is not lower than the current number of participants
        if self.id:
            participant_count = EventParticipants.objects.filter(event=self).count()
            if self.participants_limit < participant_count:
                raise ValidationError(
                    "Le nombre maximum de participants ne peut pas être inférieur au nombre actuel de participants déjà inscrits !"
                )
        
        # If it's a talk event, check if the meeting link is provided (talk_event_link)
        if self.is_talk_event:
            if not self.talk_event_link:
                logger.error(f"No Zoom link provided for talk event with ID '{self.pk}'")
                raise ValidationError("Veuillez renseigner le lien de la réunion Zoom !")

        logger.info(f"Admin form is clean. Event {self.title} with ID '{self.pk}' has been validated !")
        super().clean()

    def save(self, *args, **kwargs):
        log_debug_info("Saving event data:", self)

        if self.pk:  # Only check for existing events
            current_event = Event.objects.get(pk=self.pk)
            current_participants_limit = current_event.participants_limit
            # Is there already participants for this event ?
            if EventParticipants.objects.filter(event=self).exists():
                if self.is_fully_booked:
                    # In case event is already fully booked, check if the participants limit has been changed
                    if self.participants_limit != current_participants_limit:
                        logger.info(
                            f"Participants limit has been changed for event with ID '{self.pk}'"
                        )
                        new_limit = self.participants_limit
                        self._handle_limit_change(new_limit, current_participants_limit)
                elif not self.is_fully_booked:
                    # Has the participants limit been changed ?
                    if self.participants_limit != current_participants_limit:
                        logger.info(
                            f"Participants limit has been changed for event with ID '{self.pk}'"
                        )
                        new_limit = self.participants_limit
                        self._handle_limit_change(new_limit, current_participants_limit)

        super().save(*args, **kwargs)

    def _handle_limit_change(self, new_limit, current_limit):
        """
        If the limit has been changed by user, check if the event is now fully booked or not
        """
        if new_limit > current_limit:
            logger.info(
                f"New limit of {new_limit} is higher than the current limit of {current_limit}"
            )
            logger.info(f"Updating event with ID '{self.pk}' to not fully booked")
            # Change the event to not fully booked
            self.is_fully_booked = False
        elif new_limit < current_limit:
            logger.info(
                f"New limit of {new_limit} is lower than the current limit of {current_limit}"
            )
            logger.info(f"Checking if the event is now fully booked with the new limit")
            # Get the number of participants for this event
            participant_count = EventParticipants.objects.filter(event=self).count()
            if participant_count == new_limit:
                logger.info(
                    f"Event with ID '{self.pk}' is now fully booked with the new limit of {new_limit}"
                )
                self.is_fully_booked = True
            elif participant_count > new_limit:
                logger.warning(
                    f"The limit cannot be lower than the current number of participants ({participant_count})"
                )
                raise ValidationError(
                    "Le nombre maximum de participants ne peut pas être inférieur au nombre actuel de participants !"
                )

    def __str__(self):
        # Must check if it's a date obj to avoid err when __str__ is called (e.g : error when using log_debug_info)
        return mark_safe(
            f"{self.title} - {self.date.strftime('%d/%m/%Y') if isinstance(self.date, date) else 'Évènement sans date'}"
        )


class Participant(models.Model):
    """
    Participant model to manage the participants of the events (talk events)
    """
    fname = models.CharField(max_length=50, verbose_name="Prénom")
    lname = models.CharField(max_length=50, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = models.CharField(
        max_length=20, verbose_name="Numéro de téléphone", blank=True
    )
    address = models.CharField(max_length=100, verbose_name="Adresse")
    zip_code = models.CharField(max_length=100, verbose_name="Code postal")
    city = models.CharField(max_length=100, verbose_name="Ville")
    country = models.CharField(max_length=100, verbose_name="Pays", default="N/A")

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return self.lname + " " + self.fname


class EventParticipants(models.Model):
    """
    Model to link participants to events (Join table)
    """

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Participation"
        verbose_name_plural = "Participations"
        unique_together = ("event", "participant")

    def clean(self):
        """
        Validates the addition of a new participant to an event from the admin console.
        Checks if the event is fully booked before adding a new participant.
        """
        log_debug_info(
            "Cleaning EventParticipants object:", self, inspect_attributes=True
        )

        if not self.event.id:
            return super().clean()

        participant_id = self.participant.id
        event_instances = EventParticipants.objects.filter(event=self.event)

        if event_instances.filter(participant_id=participant_id).exists():
            return super().clean()

        logger.info(
            f"Adding participant with ID '{participant_id}' to event with ID '{self.event.id}'"
        )

        if self.event.is_fully_booked:
            logger.error(
                f"Cannot add participant. Event with ID '{self.event.id}' is fully booked."
            )
            raise ValidationError(
                "L'évènement est complet, vous ne pouvez pas ajouter ce participant !"
            )

        super().clean()

    def save(self, *args, **kwargs):
        log_debug_info(
            "Saving EventParticipants object:", self, inspect_attributes=True
        )

        # Number of participants for this event + 1 because the current participant is not yet counted
        participant_count = (
            EventParticipants.objects.filter(event=self.event).count() + 1
        )
        # Get the current limit of participants for this event
        limit = self.event.participants_limit
        logger.debug(
            f"Set limit: {limit} - Total participants for event ID '{self.event.id}': {participant_count}"
        )
        if participant_count == limit:
            logger.warning(
                f"Event {self.event.title} is now fully booked, the limit is {limit} participants"
            )
            logger.info(f"Setting event with ID '{self.event.id}' as fully booked")
            Event.objects.filter(pk=self.event.pk).update(is_fully_booked=True)
        elif participant_count > limit:
            logger.error(
                f"Event with ID '{self.event.id}' is already fully booked ! Max participants: {limit}"
            )
            raise ValidationError("L'évènement est complet !")

        log_debug_info("EventParticipants object saved successfully !")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Count the number of participants for this event minus the participant being deleted
        participant_count = (
            EventParticipants.objects.filter(event=self.event).count() - 1
        )
        # Get the limit of participants for this event
        limit = self.event.participants_limit
        logger.debug(
            f"Set limit: {limit} - Total participants for event ID '{self.event.id}': {participant_count}"
        )
        if participant_count < limit:
            logger.warning(
                f"Event {self.event.title} is no longer fully booked, the limit is {limit} participants"
            )
            logger.info(f"Setting event with ID '{self.event.id}' as not fully booked")
            Event.objects.filter(pk=self.event.pk).update(is_fully_booked=False)
        # Delete the participant
        super().delete(*args, **kwargs)

    def __str__(self):
        # Must check if it's a date obj to avoid err when __str__ is called (e.g : error when using log_debug_info)
        return f"{self.participant.email} - {self.event.title} - {self.event.date.strftime('%d/%m/%Y') if isinstance(self.event.date, date) else 'Évènement sans date'}"


class TalkEventExplanationSection(BaseSections):
    """
    Talk event explanation section, to explain to visitors how the talk events registration works
    """
    class Meta:
        verbose_name = "Page inscription aux groupes de parole"
        verbose_name_plural = "Page inscription aux groupes de parole"

    def __str__(self):
        return self.title


class MembershipSection(BaseSections):
    """
    Membership section to explain the membership process and join the association
    """
    class Meta:
        verbose_name = "Page Adhésion"
        verbose_name_plural = "Page Adhésion"

    def __str__(self):
        return self.title


class DonationSection(BaseSections):
    """
    Donation section to explain the donation process and support the association
    """
    class Meta:
        verbose_name = "Page Dons"
        verbose_name_plural = "Page Dons"

    def __str__(self):
        return self.title


class ContactSection(models.Model):
    """
    Contact section to display the contact information of the association
    """
    title = models.CharField(max_length=50, verbose_name="Titre de la section")
    text = models.TextField(
        max_length=500, verbose_name="Texte de la section (max 500 caractères)"
    )
    name = models.CharField(max_length=50, verbose_name="Nom du contact")
    email = models.EmailField(verbose_name="Email du contact")
    phone = models.CharField(
        max_length=20, verbose_name="Numéro de téléphone du contact"
    )
    address = models.CharField(max_length=100, verbose_name="Adresse du contact")

    class Meta:
        verbose_name = "Pag contact"
        verbose_name_plural = "Page contact"

    def clean(self):
        if ContactSection.objects.exists() and self.pk is None:
            raise ValidationError("Seulement une section contact est autorisée !")

    def __str__(self):
        return self.title + " - " + self.name


class AssoStatus(models.Model):
    """
    Association status model to display the association status
    """
    title = models.CharField(max_length=50, verbose_name="Titre du statut")
    richText = RichTextField(verbose_name="Texte du statut")

    class Meta:
        verbose_name = "Page statut de l'association"
        verbose_name_plural = "Page statuts de l'association"

    def clean(self):
        if AssoStatus.objects.exists() and self.pk is None:
            raise ValidationError("Seulement un statut est autorisé !")

    def __str__(self):
        return self.title


class Members(models.Model):
    """
    Members model to store the members of the association
    """
    fname = models.CharField(max_length=50, verbose_name="Prénom")
    lname = models.CharField(max_length=50, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = models.CharField(
        max_length=20, verbose_name="Numéro de téléphone", blank=True
    )
    birthdate = models.DateField(verbose_name="Date de naissance")
    address = models.CharField(max_length=100, verbose_name="Adresse")
    zip_code = models.CharField(max_length=100, verbose_name="Code postal")
    city = models.CharField(max_length=100, verbose_name="Ville")
    country = models.CharField(max_length=100, verbose_name="Pays", default="N/A")
    membership_plan = models.ForeignKey(
        "MembershipPlans", on_delete=models.CASCADE, verbose_name="Plan d'adhésion"
    )
    is_subscription_active = models.BooleanField(
        default=True, verbose_name="Adhésion active"
    )
    join_date = models.DateField(
        verbose_name="Date d'adhésion", auto_now_add=True, blank=True
    )

    class Meta:
        verbose_name = "Membre"
        verbose_name_plural = "Membres"

    def __str__(self):
        return self.lname + " " + self.fname
    
    
class MembershipPlans(models.Model):
    """
    Membership plans model to store the different membership plans
    """
    name = models.CharField(max_length=50, verbose_name="Nom du plan")
    description = models.TextField(
        max_length=500, verbose_name="Description du plan (max 500 caractères)", blank=True
    )
    price = models.DecimalField(
        max_digits=6, decimal_places=2, verbose_name="Prix du plan (CHF)"
    )
    frequency = models.CharField(
        max_length=50, verbose_name="Fréquence de paiement", default="Annuel", choices=[("yearly", "Annuel"), ("monthly", "Mensuel")]
    )
    lookup_key = models.CharField(
        max_length=50, verbose_name="Clé de recherche", unique=True
    )
    
    class Meta:
        verbose_name = "Plan d'adhésion"
        verbose_name_plural = "Plans d'adhésion"
        unique_together = ("name", "price", "frequency")
        
    def __str__(self):
        return self.name + " - " + self.frequency + " - " + str(self.price) + " CHF"