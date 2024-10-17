from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import (
    HomeSections,
    AboutSections,
    YoutubeVideos,
    AssoSections,
    ChronicTabSections,
    InvsibleTabSections,
    AdminRessources,
    TherapeuticRessources,
    LibraryRessources,
    Event,
    Participant,
    EventParticipants,
    TalkEventExplanationSection,
    ContactSection,
    AssoStatus,
    MembershipSection,
    DonationSection,
    Members,
    MembershipPlans,
    Volunteers,
)
from django.utils import timezone
from django.contrib.auth.models import User, Permission
from Invisibles23.logging_config import logger


class CustomAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        order = [
            "HomeSections",
            "AboutSections",
            "ChronicTabSections",
            "InvsibleTabSections",
            "TherapeuticRessources",
            "AdminRessources",
            "LibraryRessources",
            "AssoSections",
            "MembershipSection",
            "DonationSection",
            "TalkEventExplanationSection",
            "ContactSection",
            "AssoStatus",
            "YoutubeVideos",
            "Event",
            "Participant",
            "EventParticipants",
            "Members",
            "MembershipPlans",
            "Volunteers",
        ]
        
        # Get the original app list
        app_dict = self._build_app_dict(request)

        # Get models of website app
        app_list = app_dict["website"]["models"]

        # Sort model dictionnaries
        sorted_list = sorted(app_list, key=lambda x: order.index(x['object_name']))

        # Replace original sorted list by new one
        app_dict["website"]["models"] = sorted_list

        # Return the app list
        return app_dict.values()


class FutureEventsFilter(admin.SimpleListFilter):
    """
    A custom filter to show only future events by default.
    """

    title = "Date de l'événement"
    parameter_name = "event_time"

    def lookups(self, request, model_admin):
        return (
            ("future", "Événements futurs"),
            ("past", "Événements passés"),
        )

    def queryset(self, request, queryset):
        if self.value() == "future":
            return queryset.filter(date__gte=timezone.now())
        elif self.value() == "past":
            return queryset.filter(date__lt=timezone.now())
        return queryset


class ParticipantInline(admin.TabularInline):
    model = EventParticipants
    extra = 1


class EventAdmin(admin.ModelAdmin):
    """
    Customize the Event admin page.
    """

    list_display = (
        "date",
        "title",
        "is_talk_event",
        "is_fully_booked",
    )  # Customize fields displayed in list view
    ordering = ("-date",)  # Order by date
    search_fields = (
        "title",
        "date",
        "is_talk_event",
        "address",
        "start_time",
        "end_time",
    )  # Add search functionality
    list_filter = (
        FutureEventsFilter,
        "date",
        "is_talk_event",
    )  # Add filters for date and location
    inlines = [ParticipantInline]

    readonly_fields = ("is_fully_booked",)

    fieldsets = (
        (
            "Type d'événement",
            {
                "fields": ("is_talk_event",),
                "description": "Si il s'agit d'un événement de type 'Groupe de parole', veuillez cocher la case ci-dessus. Sinon laissez la case décochée.",
            },
        ),
        (
            "Lien de la réunion Zoom",
            {
                "fields": ("talk_event_link",),
                "description": "Si il s'agit d'un événement de type 'Groupe de parole', veuillez ajouter le lien de la réunion Zoom ici.",
            },
        ),
        (
            "Limitation du nombre de participants (si groupe de parole)",
            {
                "fields": ("participants_limit",),
                "description": "Si il s'agit d'un événement de type 'Groupe de parole', ajoutez les participants ici. Au cas où l'événement est complet mais que vous souhaitez ajouter un participant, veuillez d'abord augmenter le nombre de participants maximum, puis sauvegarder les modification et enfin ajouter le participant.",
            },
        ),
        (
            "Détails de l'événement",
            {
                "fields": ("title", "date", "start_time", "end_time"),
            },
        ),
        (
            "Informations sur l'événement",
            {
                "fields": (
                    "is_fully_booked",
                    "short_description",
                    "full_description",
                    "address",
                    "link",
                ),
            },
        ),
        (
            "Participants (groupes de parole)",
            {
                "fields": (),
                "description": "Après le paiement sur Stripe, les participants seront ajoutés automatiquement à la liste ci-dessous. Vous pouvez également ajouter des participants manuellement en cliquant sur le bouton 'Ajouter un participant'. Attention, si vous effacez un participant, il ne sera pas automatiquement remboursé.",
            },
        ),
    )

    def get_queryset(self, request):
        """
        Override the default queryset to show only future events by default.
        """
        qs = super().get_queryset(request)
        if not request.GET.get("event_time"):
            return qs.filter(date__gte=timezone.now())
        return qs


class ParticipantAdmin(admin.ModelAdmin):
    """
    Customize the Participant admin page.
    """

    list_display = (
        "email",
        "lname",
        "fname",
        "phone",
    )  # Customize fields displayed in list view
    search_fields = (
        "fname",
        "lname",
        "email",
        "phone",
    )  # Add search functionality


class MembershipPlanAdmin(admin.ModelAdmin):
    """
    Customize the MembershipPlan admin page.
    """

    list_display = (
        "name",
        "frequency",
        "price",
    )


class MembersAdmin(admin.ModelAdmin):
    """
    Customize the Members admin page.
    """

    list_display = (
        "email",
        "lname",
        "fname",
        "membership_plan",
        "join_date",
        "is_subscription_active",
    )  # Customize fields displayed in list view
    search_fields = (
        "fname",
        "lname",
        "email",
        "phone",
    )  # Add search functionality

    fieldsets = (
        (
            "Informations personnelles",
            {
                "fields": ("fname", "lname", "email", "phone", "birthdate"),
            },
        ),
        (
            "Adresse",
            {
                "fields": ("address", "city", "zip_code", "country"),
            },
        ),
        (
            "Information sur le plan d'adhésion",
            {
                "fields": ("membership_plan", "is_subscription_active"),
            },
        ),
        (
            "Informations sur le paiement",
            {
                "fields": (
                    "stripe_customer_id",
                    "payment_info_name",
                    "payment_info_country",
                ),
            },
        ),
    )


class VolunteersAdmin(admin.ModelAdmin):
    """
    Customize the Volunteers admin page.
    """

    list_display = (
        "lname",
        "fname",
        "email",
        "team",
        "phone",
        "role",
    )  # Customize fields displayed in list view
    search_fields = (
        "fname",
        "lname",
        "email",
        "phone",
    )  # Add search functionality
    fieldsets = (
        (
            "Informations personnelles",
            {
                "fields": ("fname", "lname", "email", "phone", "birthdate", "occupation"),
            },
        ),
        (
            "Adresse",
            {
                "fields": ("address", "city", "zip_code", "country"),
            },
        ),
        (
            "Informations sur le bénévole",
            {
                "fields": ("team", "role", "notes", "is_active"),
            },
        )
    )

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")

# Register the models
custom_admin_site.register(User)
custom_admin_site.register(Permission)
custom_admin_site.register(HomeSections)
custom_admin_site.register(AboutSections)
custom_admin_site.register(ChronicTabSections)
custom_admin_site.register(InvsibleTabSections)
custom_admin_site.register(TherapeuticRessources)
custom_admin_site.register(AdminRessources)
custom_admin_site.register(LibraryRessources)
custom_admin_site.register(AssoSections)
custom_admin_site.register(MembershipSection)
custom_admin_site.register(DonationSection)
custom_admin_site.register(Event, EventAdmin)
custom_admin_site.register(Participant, ParticipantAdmin)
custom_admin_site.register(EventParticipants)
custom_admin_site.register(TalkEventExplanationSection)
custom_admin_site.register(ContactSection)
custom_admin_site.register(YoutubeVideos)
custom_admin_site.register(AssoStatus)
custom_admin_site.register(Members, MembersAdmin)
custom_admin_site.register(MembershipPlans, MembershipPlanAdmin)
custom_admin_site.register(Volunteers, VolunteersAdmin)

custom_admin_site.site_header = "Les Invisibles Administration"
custom_admin_site.site_title = "Les Invisibles Admin"
custom_admin_site.index_title = "Console d'administration"
