from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .models import CustomerModel

User = get_user_model()


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        customer, _ = CustomerModel.objects.get_or_create(user=instance)
        customer.email = instance.email
        customer.save()
        subject = "Welcome to our website!"
        message_text = "Thank you for joining our community. We are excited to have you on board."

        message_html = render_to_string(
            "email/welcome_email.html",
            {
                "user": instance,
            },
        )
        recipient_list = [customer.email]
        from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMultiAlternatives(subject, message_text, from_email, recipient_list)
        email.attach_alternative(message_html, "text/html")
        email.send()