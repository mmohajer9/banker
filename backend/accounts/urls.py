from django.urls import path, include
from rest_framework import routers
from .views import AccountViewSet, JoinedRequestViewSet, TransactionViewSet

app_name = "accounts"

router = routers.SimpleRouter()

router.register("transactions", TransactionViewSet, basename="transactions")
router.register("requests", JoinedRequestViewSet, basename="requests")
router.register("", AccountViewSet, basename="")


urlpatterns = [path("", include(router.urls))]
