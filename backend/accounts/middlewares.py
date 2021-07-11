from django.conf import settings
from .models import JWTTrack
from django.http import JsonResponse, QueryDict
from rest_framework import status
import logging
import json


class BaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Code that is executed in each request before the view is called

        response = self.get_response(request)

        # Code that is executed in each request after the view is called
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # This code is executed just before the view is called
        pass

    def process_exception(self, request, exception):
        # This code is executed if an exception is raised (esp in view)
        print("EXCEPTION IS OCCURED")

    def process_template_response(self, request, response):
        # This code is executed if the response contains a render() method
        return response
