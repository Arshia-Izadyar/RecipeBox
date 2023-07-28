from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


from .managers import CustomUserManager


class User(AbstractUser):
    CONSUMER = 1
    PROVIDER = 2
    user_type = (
        (CONSUMER, "Consumer"),
        (PROVIDER, "Provider"),
    )
    
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following')
    email = models.EmailField(_("E-mail"), unique=True)
    phone_number = models.CharField(_("Phone number "), max_length=12, unique=True)
    is_admin = models.BooleanField(_("Admin status"), default=False)
    score = models.PositiveIntegerField(_("User score"), default=0)
    user_type = models.PositiveSmallIntegerField(_("User type"), choices=user_type, default=CONSUMER)

    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active. "),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "phone_number")

    objects = CustomUserManager()

    def __str__(self):
        return self.username


