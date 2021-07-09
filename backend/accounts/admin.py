from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Account, User, Transaction, JoinedRequest

# Register your models here.

admin.site.site_header = _("Banker")


admin.site.register(User, UserAdmin)


@admin.register(Account)
class AccountAdmin(SimpleHistoryAdmin):
    list_display = (
        "id",
        "user",
        "account_type",
        "conf_label",
        "integrity_label",
        "amount",
        "created_at",
        "updated_at",
    )
    # list_filter = ["user", "title", "business_phone"]
    # search_fields = ('user__username','postal_code__startswith')
    # prepopulated_fields = {'slug': ('title',)}


@admin.register(JoinedRequest)
class JoinedRequestAdmin(SimpleHistoryAdmin):
    list_display = (
        "user",
        "requested_account",
        "requested_account_conf_label",
        "requested_account_integrity_label",
        "status",
        "conf_label",
        "integrity_label",
        "has_read_access",
        "has_write_access",
        "created_at",
        "updated_at",
    )
    # list_filter = ["user", "title", "business_phone"]
    # search_fields = ('user__username','postal_code__startswith')
    # prepopulated_fields = {'slug': ('title',)}


@admin.register(Transaction)
class TransactionAdmin(SimpleHistoryAdmin):
    list_display = (
        "from_account",
        "to_account",
        "amount",
        "created_at",
        "updated_at",
    )
    # list_filter = ["user", "title", "business_phone"]
    # search_fields = ('user__username','postal_code__startswith')
    # prepopulated_fields = {'slug': ('title',)}
