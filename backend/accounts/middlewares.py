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


class AESEncryptionMiddleWare(BaseMiddleware):
    def __call__(self, request):
        # Code that is executed in each request before the view is called

        from Crypto.Cipher import AES
        from Crypto import Random
        from django.conf import settings

        enc = request.body

        key = str.encode(settings.SECRET_KEY)
        iv = enc[: AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plain_data = cipher.decrypt(enc[AES.block_size :])

        request.body = plain_data

        response = self.get_response(request)

        # Code that is executed in each request after the view is called
        return response
