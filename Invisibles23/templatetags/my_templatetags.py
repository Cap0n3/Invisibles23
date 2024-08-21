from django import template

register = template.Library()

@register.inclusion_tag('pages/components/events/event-registration-button.html')
def event_registration_button(event_pk, is_talk_event, is_fully_booked):
    """
    Event registration button with context for event_pk, is_talk_event and is_fully_booked.
    Button is displayed when event is not fully booked and display event fully booked message otherwise.
    """
    context = {
        'event_pk': event_pk,
        'is_talk_event': is_talk_event,
        'is_fully_booked': is_fully_booked,
    }
    return context

@register.inclusion_tag('pages/components/help-aside.html')
def help_aside():
    """
    Aside with help links in website forms (mebership, event registration, etc.)
    """
    return {}