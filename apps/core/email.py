from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from .utils import encode_uid


class ClientActivationEmail(BaseEmailMessage):
    template_name = "email/client_activation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        return context


class PsychoActivationEmail(BaseEmailMessage):
    template_name = "email/psycho_activation.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["protocol"] = "https"
        context["domain"] = "sharewithme.acceleratorpracticum.ru"
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context


class PsychoConfirmationFormEmail(BaseEmailMessage):
    template_name = "email/psycho_confirm_form.html"

    def get_context_data(self):
        context = super().get_context_data()

        context["email_sender"] = settings.EMAIL_SENDER
        return context


class ConfirmationEmail(BaseEmailMessage):
    template_name = "email/client_confirmation.html"


class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset_custom.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        return context


class PasswordChangedConfirmationEmail(BaseEmailMessage):
    template_name = "email/password_changed_confirm.html"


class ClientSessionCancellationEmail(BaseEmailMessage):
    template_name = "email/session_cancelled_client.html"


class PsychoSessionCancellationEmail(BaseEmailMessage):
    template_name = "email/session_cancelled_psycho.html"


class ClientNewSessionEmail(BaseEmailMessage):
    template_name = "email/session_created_client.html"


class PsychoNewSessionEmail(BaseEmailMessage):
    template_name = "email/session_created_psycho.html"
