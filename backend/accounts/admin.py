from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Account, User

# Register your models here.


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
