from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from django.utils.translation import ugettext_lazy as _
import uuid

# Create your models here.


class User(AbstractUser):
    pass


class Account(models.Model):

    CONFIDENTIALITY_CHOICES = (
        ("top-secret", "Top Secret"),
        ("secret", "Secret"),
        ("confidential", "Confidential"),
        ("unclassified", "Unclassified"),
    )

    INTEGRITY_CHOICES = (
        ("very-trusted", "Very Trusted"),
        ("trusted", "Trusted"),
        ("slightly-trusted", "Slightly Trusted"),
        ("untrusted", "Untrusted"),
    )

    ACCOUNT_TYPE_CHOCIES = (
        ("short-term", "Short Term (Kootah Modat)"),
        ("long-term", "Long Term (Boland Modat)"),
        ("current", "Current (Jari)"),
        ("gharz", "Gharz ol Hasane"),
    )

    id = models.CharField(
        primary_key=True, default=uuid.uuid1().fields[0], editable=False, max_length=10
    )

    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name=_("User"))

    account_type = models.CharField(
        max_length=100,
        choices=ACCOUNT_TYPE_CHOCIES,
        verbose_name=_("Account Type"),
        default="short-term",
    )
    conf_label = models.CharField(
        max_length=100,
        choices=CONFIDENTIALITY_CHOICES,
        verbose_name=_("Confidentiality Label"),
        default="unclassified",
    )
    integrity_label = models.CharField(
        max_length=100,
        choices=INTEGRITY_CHOICES,
        verbose_name=_("Integrity Label"),
        default="untrusted",
    )
    amount = models.DecimalField(
        _("Amount"), max_digits=10, decimal_places=2, default=0
    )

    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Updated at"), auto_now=True, blank=True, null=True
    )

    def __str__(self):
        return self.user.username

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        # unique_together = ('email',)
