from django.db import models
from django.contrib.auth.models import (
    AbstractUser,
)
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES, MinValueValidator

import uuid

# Create your models here.


class User(AbstractUser):
    def __str__(self):
        return self.username


def get_new_id():
    new_id = str(uuid.uuid1().int)
    return new_id[:10]


class Account(models.Model):

    CONFIDENTIALITY_CHOICES = (
        (4, "Top Secret"),
        (3, "Secret"),
        (2, "Confidential"),
        (1, "Unclassified"),
    )

    INTEGRITY_CHOICES = (
        (4, "Very Trusted"),
        (3, "Trusted"),
        (2, "Slightly Trusted"),
        (1, "Untrusted"),
    )

    ACCOUNT_TYPE_CHOCIES = (
        ("short-term", "Short Term (Kootah Modat)"),
        ("long-term", "Long Term (Boland Modat)"),
        ("current", "Current (Jari)"),
        ("gharz", "Gharz ol Hasane"),
    )

    id = models.CharField(
        primary_key=True, default=get_new_id, editable=False, max_length=10
    )

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="accounts",
    )

    account_type = models.CharField(
        max_length=100,
        choices=ACCOUNT_TYPE_CHOCIES,
        verbose_name=_("Account Type"),
        default="short-term",
    )
    conf_label = models.SmallIntegerField(
        choices=CONFIDENTIALITY_CHOICES,
        verbose_name=_("Confidentiality Label"),
        default=1,
    )
    integrity_label = models.SmallIntegerField(
        choices=INTEGRITY_CHOICES,
        verbose_name=_("Integrity Label"),
        default=1,
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

    history = HistoricalRecords()

    def __str__(self):
        return f"{str(self.id)} - {str(self.user)}"

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        # unique_together = ('email',)


class JoinedRequest(models.Model):

    CONFIDENTIALITY_CHOICES = (
        (4, "Top Secret"),
        (3, "Secret"),
        (2, "Confidential"),
        (1, "Unclassified"),
    )

    INTEGRITY_CHOICES = (
        (4, "Very Trusted"),
        (3, "Trusted"),
        (2, "Slightly Trusted"),
        (1, "Untrusted"),
    )

    CONFIDENTIALITY_CHOICES_DICTIONARY = {
        4: "Top Secret",
        3: "Secret",
        2: "Confidential",
        1: "Unclassified",
    }

    INTEGRITY_CHOICES_DICTIONARY = {
        4: "Very Trusted",
        3: "Trusted",
        2: "Slightly Trusted",
        1: "Untrusted",
    }

    STATUS_CHOICES = [
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    ]

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name=_("Applicant User"),
        related_name="joined_requests",
    )
    conf_label = models.SmallIntegerField(
        choices=CONFIDENTIALITY_CHOICES,
        verbose_name=_("Requested Confidentiality Label"),
        default=1,
    )

    integrity_label = models.SmallIntegerField(
        choices=INTEGRITY_CHOICES,
        verbose_name=_("Requested Integrity Label"),
        default=1,
    )
    requested_account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        verbose_name=_("Requested Account"),
        related_name="joined_requests",
    )
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        verbose_name=_("Status"),
        default="pending",
    )

    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Updated at"), auto_now=True, blank=True, null=True
    )

    history = HistoricalRecords()

    def __str__(self):
        return str(self.requested_account.user)

    def clean(self):
        if self.user == self.requested_account.user:
            raise ValidationError(_("You can not request to yourself"))
        return super().clean()

    def requested_account_conf_label(self):
        return self.CONFIDENTIALITY_CHOICES_DICTIONARY[
            self.requested_account.conf_label
        ]

    requested_account_conf_label.short_description = _("Account Confidentiality Label")

    def requested_account_integrity_label(self):
        return self.INTEGRITY_CHOICES_DICTIONARY[self.requested_account.integrity_label]

    requested_account_integrity_label.short_description = _("Account Integrity Label")

    def has_read_access(self):
        subject_conf = self.conf_label
        subject_integrity = self.integrity_label
        object_conf = self.requested_account.conf_label
        object_integrity = self.requested_account.integrity_label

        return bool(
            subject_conf >= object_conf and subject_integrity <= object_integrity
        )

    has_read_access.short_description = _("Has Read Access")
    has_read_access.boolean = True

    def has_write_access(self):
        subject_conf = self.conf_label
        subject_integrity = self.integrity_label
        object_conf = self.requested_account.conf_label
        object_integrity = self.requested_account.integrity_label

        return bool(
            subject_conf <= object_conf and subject_integrity >= object_integrity
        )

    has_write_access.short_description = _("Has Write Access")
    has_write_access.boolean = True

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = "Joined Request"
        verbose_name_plural = "Joined Requests"
        unique_together = (
            "user",
            "requested_account",
        )


class Transaction(models.Model):

    TRANSACTION_TYPE_CHOICES = (
        ("deposit", "Deposit"),
        ("withdraw", "Withdraw"),
    )

    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        related_name="transactions",
        null=True,
        blank=True,
    )

    from_account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        verbose_name=_("From"),
        blank=True,
        null=True,
        related_name="transactions_as_sender",
    )

    to_account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        verbose_name=_("To"),
        related_name="transactions_as_reciever",
    )
    transaction_type = models.CharField(
        max_length=100,
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name=_("Transaction Type"),
        default="deposit",
    )
    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(1)],
    )

    created_at = models.DateTimeField(
        _("Created at"), auto_now_add=True, blank=True, null=True
    )
    updated_at = models.DateTimeField(
        _("Updated at"), auto_now=True, blank=True, null=True
    )

    def __str__(self):
        return f"{self.from_account} > {self.to_account} : {self.amount}"

    def clean(self):

        if self.transaction_type == "deposit":
            if self.from_account not in EMPTY_VALUES:
                raise ValidationError(
                    {
                        "from_account": _(
                            "In deposit, you can not specify source account"
                        )
                    }
                )

        elif self.transaction_type == "withdraw":
            if self.from_account in EMPTY_VALUES:
                raise ValidationError(
                    {
                        "from_account": _(
                            "In withdraw, you should specify source account"
                        )
                    }
                )

            if self.from_account == self.to_account:
                raise ValidationError(
                    {
                        "from_account": _(
                            "source account can not be the same as destination"
                        ),
                        "to_account": _(
                            "source account can not be the same as destination"
                        ),
                    }
                )

            if self.from_account.amount < self.amount:
                raise ValidationError(
                    {"amount": _("Not enough balance in the source account")}
                )

            joined_request = JoinedRequest.objects.filter(
                user=self.user,
                requested_account=self.from_account,
                status="accepted",
            )

            if joined_request.exists():
                if not joined_request.first().has_write_access():
                    raise ValidationError(
                        {
                            "user": _(
                                "This user does not have access to the source account because of low access level"
                            )
                        }
                    )
            else:
                if not self.from_account.user == self.user:
                    raise ValidationError(
                        {
                            "user": _(
                                "This user does not have access to the source account because of low access level"
                            )
                        }
                    )

        return super().clean()

    class Meta:
        # db_table = ''
        # managed = True
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
