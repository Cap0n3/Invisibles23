from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import (
    HomeSections,
    AboutSections,
    YoutubeVideos,
    AssoSections,
    ChronicTabSections,
    InvsibleTabSections,
    MiscarriageTabSections,
    AdminRessources,
    TherapeuticRessources,
    FinancialRessources,
    Event,
    ContactSection,
    AssoStatus,
    MembershipSection,
    DonationSection,
)

class CustomAdminSite(AdminSite):
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
            "Home sections": 1,
            "About sections": 2,
            "Youtube videos": 3,
            "Asso sections": 4,
            "Chronic tab sections": 5,
            "Invsible tab sections": 6,
            "Miscarriage tab sections": 7,
            "Admin ressources": 8,
            "Therapeutic ressources": 9,
            "Financial ressources": 10,
            "Events": 11,
            "Contact sections": 12,
            "Asso statuses": 13,
            "Membership sections": 14,
            "Donation sections": 15,
        }
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        for app in app_list:
            app['models'].sort(key=lambda x: ordering.get(x['name'], float('inf')))
        
        return app_list

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

custom_admin_site.register(HomeSections)
custom_admin_site.register(AboutSections)
custom_admin_site.register(YoutubeVideos)
custom_admin_site.register(AssoSections)
custom_admin_site.register(ChronicTabSections)
custom_admin_site.register(InvsibleTabSections)
custom_admin_site.register(MiscarriageTabSections)
custom_admin_site.register(AdminRessources)
custom_admin_site.register(TherapeuticRessources)
custom_admin_site.register(FinancialRessources)
custom_admin_site.register(Event)
custom_admin_site.register(ContactSection)
custom_admin_site.register(AssoStatus)
custom_admin_site.register(MembershipSection)
custom_admin_site.register(DonationSection)

# Register your models here.
# admin.site.register(HomeSections)
# admin.site.register(AboutSections)
# admin.site.register(YoutubeVideos)
# admin.site.register(AssoSections)
# admin.site.register(ChronicTabSections)
# admin.site.register(InvsibleTabSections)
# admin.site.register(MiscarriageTabSections)
# admin.site.register(AdminRessources)
# admin.site.register(TherapeuticRessources)
# admin.site.register(FinancialRessources)
# admin.site.register(Event)
# admin.site.register(ContactSection)
# admin.site.register(AssoStatus)
# admin.site.register(MembershipSection)
# admin.site.register(DonationSection)
