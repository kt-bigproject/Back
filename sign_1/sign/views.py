import pickle

import numpy as np
from PIL.Image import Image
from django.shortcuts import render
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC


# class ConfirmEmailView(APIView):
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#         confirmation = self.get_object()
#         confirmation.confirm(self.request)
#         # 성공 시나리오는 React Router Route가 처리할 것입니다.
#         return Response({'message': 'Email confirmed successfully.'})
#
#     def get_object(self):
#         key = self.kwargs['key']
#         email_confirmation = EmailConfirmationHMAC.from_key(key)
#         if not email_confirmation:
#             raise NotFound('Email confirmation not found.')
#         return email_confirmation
#
#     def get_queryset(self):
#         qs = EmailConfirmation.objects.all_valid()
#         qs = qs.select_related("email_address__user")
#         return qs
class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        # 성공 시나리오는 React Router Route가 처리할 것입니다.
        return Response({'message': 'Email confirmed successfully.'})

    def get_object(self):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            raise NotFound('Email confirmation not found.')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


