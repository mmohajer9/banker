from .models import AuditLog, JoinedRequest
from rest_framework.permissions import BasePermission, SAFE_METHODS

# from django.contrib.auth.models import AnonymousUser


class SampleCustomPermission(BasePermission):

    """First Priority : has_permission() will be executed for the first time"""

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    # ONLY FOR A API VIEW THAT IS DEDICATED FOR A SPECIFIC OBJECT LIKE : RetrieveUpdateAPIView and not like : ListAPIView
    """After the first priority the second priority that is has_object_permission() will be executed"""

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class HasReadAccess(BasePermission):

    # ONLY FOR A API VIEW THAT IS DEDICATED FOR A SPECIFIC OBJECT LIKE : RetrieveUpdateAPIView and not like : ListAPIView
    """After the first priority the second priority that is has_object_permission() will be executed"""

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            jr = JoinedRequest.objects.get(
                user=request.user,
                requested_account=obj,
                status="accepted",
            )

            if jr.has_read_access():
                return True
            else:

                AuditLog.objects.create(
                    action="Access Control : No Read Access",
                    path=request.path,
                    method=request.method,
                    user=request.user,
                    remote_address=request.META.get("REMOTE_ADDR"),
                    content_type=request.META.get("CONTENT_TYPE"),
                    log_name=request.META.get("LOGNAME"),
                    browser=request.META.get("BROWSER"),
                    user_agent=request.META.get("HTTP_USER_AGENT"),
                )

                return False

        except:
            return True


class HasWriteAccess(BasePermission):

    # ONLY FOR A API VIEW THAT IS DEDICATED FOR A SPECIFIC OBJECT LIKE : RetrieveUpdateAPIView and not like : ListAPIView
    """After the first priority the second priority that is has_object_permission() will be executed"""

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            jr = JoinedRequest.objects.get(
                user=request.user,
                requested_account=obj,
                status="accepted",
            )

            return jr.has_write_access()

        except:
            return True


class Forbidden(BasePermission):

    """First Priority : has_permission() will be executed for the first time"""

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return False
