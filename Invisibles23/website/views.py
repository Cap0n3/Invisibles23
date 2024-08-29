from typing import Any
from django.shortcuts import render
from django.views import View
from Invisibles23.logging_config import logger
from Invisibles23.logging_utils import log_debug_info
from .forms import MembershipForm, EventRegistrationForm
from .utils.view_helpers import createFormErrorContext
from datetime import date
from .models import (
    HomeSections,
    AboutSections,
    AssoSections,
    ChronicTabSections,
    InvsibleTabSections,
    AdminRessources,
    TherapeuticRessources,
    FinancialRessources,
    MiscarriageTabSections,
    YoutubeVideos,
    Event,
    Participant,
    EventParticipants,
    ContactSection,
    AssoStatus,
    MembershipSection,
    DonationSection,
)
from .filters import (
    AdminRessourcesFilter,
    TherapeuticRessourcesFilter,
    FinancialRessourcesFilter,
)
from django.http import JsonResponse
import environ
from django.middleware.csrf import get_token
from django.conf import settings
from django.shortcuts import redirect
import stripe


# Initialise env vars
env = environ.Env()
env.read_env("../.env")


# == Base view classes to stay DRY == #
class BaseThematicView(View):
    """
    Base class for the thematic views
    """

    template_name = None
    # queryset = None

    def get_queryset(self):
        return {
            "sections_content": getattr(self, "model", None).objects.exclude(
                order=0
            )  # Get section from the given model
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class BaseRessourcesView(View):
    """
    Base class for the ressources views
    """

    template_name = "pages/ressources.html"
    filter_class = None

    def get_queryset(self):
        queryset = getattr(
            self, "model", None
        ).objects.all()  # Get all objects from the given model
        return queryset

    def get_context_data(self):
        filter_form = self.filter_class(self.request.GET, queryset=self.get_queryset())
        ressources = filter_form.qs
        return {"ressources": ressources, "filter_form": filter_form}

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)


# == Views == #
class HomeView(View):
    template_name = "pages/home.html"
    # queryset = HomeSections.objects.all()
    # contact_query = ContactSection.objects.first() # For the contact form

    def get_queryset(self):
        # return Home section and contact section queryset
        return {
            "sections_content": HomeSections.objects.all(),
            "contact_content": ContactSection.objects.first(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = "pages/about.html"

    def get_queryset(self):
        # return About section and all videos queryset
        return {
            "sections_content": AboutSections.objects.all(),
            "videos": YoutubeVideos.objects.all(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class ChronicTabView(BaseThematicView):
    template_name = "pages/chronic.html"
    model = ChronicTabSections  # Model to query


class InvisibleTabView(BaseThematicView):
    template_name = "pages/invisible.html"
    model = InvsibleTabSections  # Model to query


class MiscarriageTabView(BaseThematicView):
    template_name = "pages/miscarriage.html"
    model = MiscarriageTabSections  # Model to query


class PodcastsView(View):
    template_name = "pages/podcasts.html"

    def get(self, request):
        return render(request, self.template_name, {})


class AdminRessourcesView(BaseRessourcesView):
    model = AdminRessources
    filter_class = AdminRessourcesFilter


class TherapeuticRessourcesView(BaseRessourcesView):
    model = TherapeuticRessources
    filter_class = TherapeuticRessourcesFilter


class FinancialRessourcesView(BaseRessourcesView):
    model = FinancialRessources
    filter_class = FinancialRessourcesFilter


class AssociationView(View):
    template_name = "pages/association.html"

    def get_queryset(self):
        return {
            "sections_content": AssoSections.objects.all(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class EventListView(View):
    template_name = "pages/events-list.html"
    queryset = Event.objects.all()

    def get_queryset(self):
        # Get future events and order them by date
        return {
            "events_content": self.queryset.filter(date__gte=date.today()).order_by(
                "date"
            ),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class EventDetailView(View):
    template_name = "pages/event-detail.html"

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        context = {
            "event": event,
        }
        return render(request, self.template_name, context)


class EventRegistrationView(View):
    """
    View to handle the event (talk group) registration form and the Stripe checkout session.
    Lookup keys are used to get the prices from Stripe :
    - talkGroup-registration-reduced
    - talkGroup-registration-normal
    - talkGroup-registration-support
    """

    template_name = "pages/event-registration.html"

    def get(self, request, pk):
        event = Event.objects.get(pk=pk)
        form = EventRegistrationForm(initial={"event": event.pk})
        context = {
            "form": form,
            "event": event,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        form = EventRegistrationForm(request.POST)
        domain = (
            "http://127.0.0.1:8000" if settings.DEBUG else f"https://{settings.DOMAIN}"
        )
        stripe.api_key = env("STRIPE_API_TOKEN")

        log_debug_info("||====== DEBUG MODE IS ON ! ======||")
        log_debug_info("Domain", domain)
        log_debug_info("Request data", request.POST)

        if form.is_valid():
            logger.info("Event registration form is valid")
            membership_status = form.cleaned_data["membership_status"]
            plan = form.cleaned_data["plan"]
            first_name = form.cleaned_data["fname"]
            last_name = form.cleaned_data["lname"]
            phone = form.cleaned_data["phone"]
            address = form.cleaned_data["address"]
            zip_code = form.cleaned_data["zip_code"]
            city = form.cleaned_data["city"]
            email = form.cleaned_data["email"]

            # Get the event
            try:
                event = Event.objects.get(pk=pk)
                logger.info(f"Event found: {event}")
            except Event.DoesNotExist:
                logger.error(f"Event with ID {pk} does not exist")
                return render(
                    request,
                    self.template_name,
                    {"form": form, "error_messages": "L'événement n'existe pas."},
                )

            # Check if participant is already registered with this event
            if Participant.objects.filter(email=email).exists():
                participant = Participant.objects.get(email=email)
                logger.info(
                    f"Participant is already in the database: {participant.email}"
                )

                if EventParticipants.objects.filter(
                    event=event, participant=participant
                ).exists():
                    logger.warning(
                        f"Participant already registered for this event: {event}, it'll be redirected to the event page"
                    )
                    return render(
                        request,
                        self.template_name,
                        {
                            "form": form,
                            "event": event,
                            "error_messages": f"Il semblerait que vous soyez déjà inscrit à cet événement. Si vous avez des questions, veuillez nous contacter à l'adresse suivante",
                        },
                    )

            # Create metadata for the checkout session
            metadata = {
                "event_id": event.id,
                "event_infos": f"{event.date} - {event.title}",
                "event_description": event.short_description,
                "fname": first_name,
                "lname": last_name,
                "phone": phone,
                "membership_status": membership_status,
                "address": address,
                "zip_code": zip_code,
                "city": city,
                "customer_email": email,
                "type": "talk-group",
            }

            # Create lookup key based on the plan
            lookup_key = f"talkGroup-registration-{plan}"

            log_debug_info("Metadata", metadata)
            log_debug_info("Lookup key", lookup_key)

            try:
                # Get prices from Stripe
                logger.info("Getting prices from Stripe ...")
                prices = stripe.Price.list(
                    lookup_keys=[lookup_key], expand=["data.product"]
                )

                log_debug_info("Prices list", prices)

                # Create checkout session to redirect to Stripe
                logger.info("Creating checkout session ...")
                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            "price": prices.data[0].id,
                            "quantity": 1,
                        },
                    ],
                    currency="chf",
                    allow_promotion_codes=True,
                    customer_email=email,
                    metadata=metadata,
                    payment_intent_data={
                        "metadata": metadata,
                    },
                    custom_text={
                        "submit": {
                            "message": "Si vous êtes membres de l'association, n'oubliez pas d'appliquer votre code promo lors du paiement (colonne de gauche).",
                        },
                        "after_submit": {
                            "message": "Vous serrez redirigé vers le site de l'association après le paiement sécurisé.",
                        },
                    },
                    mode="payment",
                    success_url=domain + "/success/",
                    cancel_url=domain + "/rendez-vous/",
                )

                logger.info("Session created successfully ... redirecting to checkout")
                log_debug_info("Session url", checkout_session["url"])

                return redirect(checkout_session["url"], code=303)

            except Exception as error:
                logger.error(
                    f"(EventRegistrationView) -> An exception occurred: {error}"
                )
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "error_messages": f"An error occurred during the request. Please try again later or contact us at the following address: {settings.DEV_EMAIL}",
                    },
                )
        else:
            error_context = createFormErrorContext(form)
            return render(request, self.template_name, error_context)


class ContactView(View):
    template_name = "pages/contact.html"

    def get_queryset(self):
        # return Home section and contact section queryset
        return {
            "contact_content": ContactSection.objects.first(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class MembershipView(View):
    template_name = "pages/membership.html"
    form_class = MembershipForm()
    initial_form_state = {
        "subscription": "normal",
        "frequency": "yearly",
    }  # Default state of radio buttons

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.domain = (
            "http://127.0.0.1:8000" if settings.DEBUG else f"https://{settings.DOMAIN}"
        )
        self.subscription = None
        self.frequency = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.phone = None
        self.birthday = None
        self.address = None
        self.zip_code = None
        self.city = None
        self.country = None
        self.lookup_key = None
        self.prices = None
        self.checkout_session_object = None

    def get_queryset(self):
        # Text for the membership adhesion
        return {
            "sections_content": MembershipSection.objects.all(),
        }

    def get(self, request):
        form = MembershipForm(initial=self.initial_form_state)
        sections = self.get_queryset()
        context = {
            "form": form,
            "sections_content": sections["sections_content"],
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = MembershipForm(request.POST)
        stripe.api_key = env("STRIPE_API_TOKEN")
        log_debug_info("Request data", request.POST)

        if form.is_valid():
            logger.info("Membership form is valid")

            try:
                self._extract_form_data(form)
                # Check if customer already exists
                if self._check_already_has_active_subscription():
                    return render(
                        request,
                        self.template_name,
                        {
                            "form": form,
                            "error_messages": f"Vous êtes déjà membre de notre association ! Si vous souhaitez modifier votre abonnement, veuillez nous contacter à l'adresse suivante : {settings.OWNER_EMAIL}",
                        },
                    )

                self._create_lookup_key()
                self._get_stripe_price_list()
                self._create_checkout_session()

                return redirect(self.checkout_session_object["url"], code=303)

            except Exception as error:
                logger.error(f"(MembershipView) -> An exception occurred: {error}")
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "error_messages": f"Une erreur s'est produite lors de la demande. Veuillez réessayer plus tard ou nous contacter à l'adresse suivante : {settings.DEV_EMAIL}",
                    },
                )

        else:
            error_context = createFormErrorContext(form)
            return render(request, self.template_name, error_context)

    def _extract_form_data(self, form) -> None:
        """
        Extracts the data from the form and assigns it to the class attributes.
        """
        try:
            self.subscription = form.cleaned_data["subscription"]
            self.frequency = form.cleaned_data["frequency"]
            self.first_name = form.cleaned_data["fname"]
            self.last_name = form.cleaned_data["lname"]
            self.email = form.cleaned_data["email"]
            self.phone = form.cleaned_data["phone"]
            self.birthday = form.cleaned_data["birthday"]
            self.address = form.cleaned_data["address"]
            self.zip_code = form.cleaned_data["zip_code"]
            self.city = form.cleaned_data["city"]
            self.country = form.cleaned_data["country"]
        except Exception as error:
            logger.error(f"An exception occurred while extracting form data: {error}")
            raise error

    def _check_already_has_active_subscription(self) -> bool:
        """
        This function checks if a customer already exists in the Stripe database and
        if the customer exists, it will check if they have an active subscription.

        Returns
        -------
        bool
            True if the customer already has an active subscription, False otherwise
        """
        logger.info("Checking if customer already exists ...")

        try:
            # Search for customer
            customer_search = stripe.Customer.search(
                query=f"name:'{self.first_name} {self.last_name}' AND email:'{self.email}'",
            )
        except Exception as error:
            logger.error(f"An exception occurred: {error}")
            raise error

        if customer_search:
            logger.warning(f"Customer already exists: {customer_search.data[0]}")
            existing_customer_id = customer_search.data[0].id
            # Search for active subscription
            try:
                subscription_search = stripe.Subscription.search(
                    query=f"status:'active'",
                )
            except Exception as error:
                logger.error(f"An exception occurred: {error}")
                raise error
            else:
                # Loop through subscriptions and find the one with the customer ID
                for subscription in subscription_search.data:
                    if subscription.customer == existing_customer_id:
                        logger.warning(
                            f"Customer already has an active subscription: {subscription}"
                        )
                        return True
        return False

    def _create_lookup_key(self) -> None:
        """
        This function creates a lookup key based on the subscription and frequency.

        It will return following values:
        - support-monthly
        - support-yearly
        - normal-monthly
        - normal-yearly
        - reduced-monthly
        - reduced-yearly
        """
        if self.subscription == "support":
            self.lookup_key = (
                "support-monthly" if self.frequency == "monthly" else "support-yearly"
            )
        elif self.subscription == "normal":
            self.lookup_key = (
                "normal-monthly" if self.frequency == "monthly" else "normal-yearly"
            )
        elif self.subscription == "reduced":
            self.lookup_key = (
                "reduced-monthly" if self.frequency == "monthly" else "reduced-yearly"
            )
        else:
            logger.error(
                f"Invalid subscription or frequency: {self.subscription}, {self.frequency}"
            )
            raise ValueError("Invalid subscription or frequency")

    def _get_stripe_price_list(self) -> None:
        """
        This function gets the prices from Stripe based on the lookup key.
        """
        try:
            # Get prices from Stripe
            logger.info("Getting prices from Stripe ...")
            self.prices = stripe.Price.list(
                lookup_keys=[self.lookup_key], expand=["data.product"]
            )
            log_debug_info("Prices list", self.prices)
        except Exception as error:
            logger.error(f"An exception occurred: {error}")
            raise error

    def _create_checkout_session(self) -> None:
        """
        This function creates a checkout session for the membership subscription.
        It also creates metadata that will be used to store the member's information.
        """
        logger.info("Creating checkout session ...")
        try:
            self.checkout_session_object = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": self.prices.data[0].id,
                        "quantity": 1,
                    },
                ],
                currency="chf",
                customer_email=self.email,
                subscription_data={
                    "metadata": {
                        "name": f"{self.first_name} {self.last_name}",
                        "customer_email": self.email,
                        "phone": self.phone,
                        "birthday": self.birthday,
                        "address": self.address,
                        "zip_code": self.zip_code,
                        "city": self.city,
                        "country": self.country,
                        "type": "membership",
                    },
                },
                metadata={
                    "name": f"{self.first_name} {self.last_name}",
                    "customer_email": self.email,
                    "phone": self.phone,
                    "birthday": self.birthday,
                    "address": self.address,
                    "zip_code": self.zip_code,
                    "city": self.city,
                    "country": self.country,
                    "type": "membership",
                },
                mode="subscription",
                success_url=self.domain + "/success/",
                cancel_url=self.domain + "/membership/",
            )
        except Exception as error:
            logger.error(f"An exception occurred: {error}")
            raise error
        else:
            logger.info("Session created successfully ... redirecting to checkout")
            log_debug_info("Session url", self.checkout_session_object["url"])


class DonationView(View):
    template_name = "pages/donation.html"

    def get_queryset(self):
        # Text for the donation adhesion
        return {
            "sections_content": DonationSection.objects.all(),
        }

    def get(self, request):
        context = self.get_queryset()
        return render(request, self.template_name, context)


class StatusView(View):
    template_name = "pages/status.html"

    def get_queryset(self):
        # return Home section and contact section queryset
        return AssoStatus.objects.first()

    def get(self, request):
        context = {
            "status_content": self.get_queryset(),
        }
        return render(request, self.template_name, context)


class SuccessView(View):
    template_name = "pages/success.html"

    def get(self, request):
        logger.info("Payment successful ... redirecting to success page")
        return render(request, self.template_name, {})


class Custom404View(View):
    def get(self, request, exception=None):
        return render(request, "pages/404.html", status=404)


def get_sensitive_info(request):
    data = {
        "ausha_api_token": env("AUSHA_API_TOKEN"),
        "mailchimp_api_key": env("MAILCHIMP_API_KEY"),
        "mailchimp_list_id": env("MAILCHIMP_LIST_ID"),
        "emailjs_service_id": env("EMAILJS_SERVICE_ID"),
        "emailjs_template_id": env("EMAILJS_TEMPLATE_ID"),
        "emailjs_user_id": env("EMAILJS_USER_ID"),
    }

    return JsonResponse(data)
