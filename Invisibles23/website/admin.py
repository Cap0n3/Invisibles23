from django.contrib import admin
from .models import (
    HomePageSections, 
    AboutPageSections, 
    YoutubeVideos, 
    AssociationSections,
    ChronicTabSections,
    InvsibleTabSections,
    MiscarriageTabSections,
    AdminRessources,
    TherapeuticRessources,
    FinancialRessources,
    Event,
    ContactSection
)

# Register your models here.
admin.site.register(HomePageSections)
admin.site.register(AboutPageSections)
admin.site.register(YoutubeVideos)
admin.site.register(AssociationSections)
admin.site.register(ChronicTabSections)
admin.site.register(InvsibleTabSections)
admin.site.register(MiscarriageTabSections)
admin.site.register(AdminRessources)
admin.site.register(TherapeuticRessources)
admin.site.register(FinancialRessources)
admin.site.register(Event)
admin.site.register(ContactSection)
