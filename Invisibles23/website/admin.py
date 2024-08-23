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
    FinancialRessources,
    Event,
    Participant,
    EventParticipants,
    ContactSection,
    AssoStatus,
    MembershipSection,
    DonationSection,
)
from django.utils import timezone


class CustomAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Home sections": 1,
            "About sections": 2,
            "Chronic tab sections": 3,
            "Invsible tab sections": 4,
            "Therapeutic ressources": 5,
            "Admin ressources": 6,
            "Financial ressources": 7,
            "Asso sections": 8,
            "Membership sections": 9,
            "Donation sections": 10,
            "Events": 11,
            "Contact sections": 12,
            "Youtube videos": 13,
            "Asso statuses": 14,
        }
        app_dict = self._build_app_dict(request)

        # Sort apps based on the ordering dictionary
        app_list = sorted(
            app_dict.values(), key=lambda x: ordering.get(x["name"], float("inf"))
        )

        for app in app_list:
            app["models"].sort(key=lambda x: ordering.get(x["name"], float("inf")))

        return app_list


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
            "Participants",
            {
                "fields": (),
                "description": "Après le paiement sur Stripe, les participants seront ajoutés automatiquement à la liste ci-dessous. Vous pouvez également ajouter des participants manuellement en cliquant sur le bouton 'Ajouter un participant'. Attention, si vous effacer un participant, il ne sera pas automatiquement remboursé.",
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

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")

# Register the models
custom_admin_site.register(HomeSections)
custom_admin_site.register(AboutSections)
custom_admin_site.register(ChronicTabSections)
custom_admin_site.register(InvsibleTabSections)
custom_admin_site.register(TherapeuticRessources)
custom_admin_site.register(AdminRessources)
custom_admin_site.register(FinancialRessources)
custom_admin_site.register(AssoSections)
custom_admin_site.register(MembershipSection)
custom_admin_site.register(DonationSection)
custom_admin_site.register(Event, EventAdmin)
custom_admin_site.register(Participant, ParticipantAdmin)
custom_admin_site.register(EventParticipants)
custom_admin_site.register(ContactSection)
custom_admin_site.register(YoutubeVideos)
custom_admin_site.register(AssoStatus)

custom_admin_site.site_header = "Les Invisibles Administration"
custom_admin_site.site_title = "Les Invisibles Admin"
custom_admin_site.index_title = "Console d'administration"
