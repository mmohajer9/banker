from rest_framework import throttling


class AuditedScopedThrottle(throttling.ScopedRateThrottle):
    def throttle_failure(self):
        request = self.request._request

        # print(request.path)
        # print(request.method)
        # print(request.user)
        # print(request.auth)
        # print(request.META.get('REQUEST_METHOD'))
        # print(request.META.get('REMOTE_ADDR'))
        # print(request.META.get('CONTENT_TYPE'))
        # print(request.META.get('LOGNAME'))
        # print(request.META.get('BROWSER'))
        # print(request.META.get('USER'))
        # print(request.META.get('HTTP_USER_AGENT'))
        
        return super().throttle_failure()

    def allow_request(self, request, view):

        self.request = request
        self.view = view

        return super().allow_request(request, view)
