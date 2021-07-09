from rest_framework import viewsets
from rest_framework import permissions

# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

from .generics import EnhancedModelViewSet
from .permissions import Forbidden
from .models import Account


# Create your views here.


class AccountViewSet(EnhancedModelViewSet):

    queryset = Account.objects.all()

    pagination_class = CustomLimitOffsetPagination
    # default serializer and permission classes
    serializer_class = SellerSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filterset_class = SellerFilter
    search_fields = ["title", "business_phone", "description", "user__username"]
    ordering_fields = "__all__"
    ordering = ["id"]

    # override per action
    action_serializers = {
        # "list": Serializer1,
        # "create": Serializer2,
        "retrieve": SellerDetailSerializer,
        # "update": Serializer4,
        # "partial_update": Serializer5,
        # "destroy": Serializer6,
    }

    # override per action
    action_permission_classes = {
        "list": [permissions.AllowAny],
        "create": [permissions.IsAuthenticated, IsNotSeller],
        "retrieve": [permissions.AllowAny],
        "update": [permissions.IsAuthenticated, IsOwner],
        "partial_update": [permissions.IsAuthenticated, IsOwner],
        "destroy": [permissions.IsAuthenticated, IsOwner],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    lookup_field = "user__username"