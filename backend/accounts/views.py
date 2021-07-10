from rest_framework import viewsets
from rest_framework import permissions
from django.db.models import Q

# from rest_framework.response import Response
# from django.shortcuts import get_object_or_404

from .generics import EnhancedModelViewSet
from .serializers import (
    AccountSerializer,
    JoinedRequestCreateSerializer,
    JoinedRequestSerializer,
    JoinedRequestUpdateSerializer,
    TransactionSerializer,
)
from .permissions import Forbidden, HasReadAccess
from .models import Account, JoinedRequest, Transaction


# Create your views here.


class AccountViewSet(EnhancedModelViewSet):
    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(
            Q(user=user)
            | Q(joined_requests__user=user, joined_requests__status="accepted")
        )

    # default serializer and permission classes
    serializer_class = AccountSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    ordering_fields = "__all__"
    ordering = ["id"]

    # override per action
    # action_serializers = {
    #     # "list": Serializer1,
    #     # "create": Serializer2,
    #     # "retrieve": SellerDetailSerializer,
    #     # "update": Serializer4,
    #     # "partial_update": Serializer5,
    #     # "destroy": Serializer6,
    # }

    # # override per action
    action_permission_classes = {
        "list": [permissions.IsAuthenticated],
        "create": [permissions.IsAuthenticated],
        "retrieve": [permissions.IsAuthenticated, HasReadAccess],
        "update": [Forbidden],
        "partial_update": [Forbidden],
        "destroy": [Forbidden],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JoinedRequestViewSet(EnhancedModelViewSet):
    def get_queryset(self):
        return JoinedRequest.objects.filter(requested_account__user=self.request.user)

    # default serializer and permission classes
    serializer_class = JoinedRequestSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    ordering_fields = "__all__"
    ordering = ["id"]

    # override per action
    action_serializers = {
        "list": JoinedRequestSerializer,
        "create": JoinedRequestCreateSerializer,
        # "retrieve": JoinedRequestSerializer,
        "update": JoinedRequestUpdateSerializer,
        "partial_update": JoinedRequestUpdateSerializer,
        # "destroy": Serializer6,
    }

    # # override per action
    action_permission_classes = {
        "list": [permissions.IsAuthenticated],
        "create": [permissions.IsAuthenticated],
        "retrieve": [
            permissions.IsAuthenticated,
        ],
        "update": [
            permissions.IsAuthenticated,
        ],
        "partial_update": [
            permissions.IsAuthenticated,
        ],
        "destroy": [Forbidden],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(EnhancedModelViewSet):
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    # default serializer and permission classes
    serializer_class = TransactionSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    ordering_fields = "__all__"
    ordering = ["id"]

    # override per action
    # action_serializers = {
    #     "list": JoinedRequestSerializer,
    #     "create": JoinedRequestCreateSerializer,
    #     # "retrieve": JoinedRequestSerializer,
    #     "update": JoinedRequestUpdateSerializer,
    #     "partial_update": JoinedRequestUpdateSerializer,
    #     # "destroy": Serializer6,
    # }

    # # override per action
    action_permission_classes = {
        "list": [permissions.IsAuthenticated],
        "create": [permissions.IsAuthenticated],
        "retrieve": [permissions.IsAuthenticated],
        "update": [Forbidden],
        "partial_update": [Forbidden],
        "destroy": [Forbidden],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
