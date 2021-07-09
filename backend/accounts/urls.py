from django.urls import path, include
from rest_framework import routers

app_name = "accounts"

router = routers.SimpleRouter()

urlpatterns = [path("", include(router.urls))]
