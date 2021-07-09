from django.urls import path, include
from rest_framework import routers
from .views import AccountViewSet

app_name = "accounts"

router = routers.SimpleRouter()

router.register("", AccountViewSet, basename="")


urlpatterns = [path("", include(router.urls))]
