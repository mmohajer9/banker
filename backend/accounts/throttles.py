from .models import AuditLog
from rest_framework import throttling


class AuditedScopedThrottle(throttling.ScopedRateThrottle):
    def throttle_failure(self):
        request = self.request._request

        AuditLog.objects.create(
            action="Wrong Password Throttle",
            path=request.path,
            method=request.method,
            user=request.user,
            remote_address=request.META.get("REMOTE_ADDR"),
            content_type=request.META.get("CONTENT_TYPE"),
            log_name=request.META.get("LOGNAME"),
            browser=request.META.get("BROWSER"),
            user_agent=request.META.get("HTTP_USER_AGENT"),
        )

        return super().throttle_failure()

    def allow_request(self, request, view):

        self.request = request
        self.view = view

        return super().allow_request(request, view)
