from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, authentication, permissions


@api_view()
def first_drf_view(request):
    """
    Return a simple JSON object.
    """
    return Response({"message": "Got a GET request!"})


@api_view(['GET', 'POST'])
def multi_method_view(request):
    """
    If received a POST request, return a JSON object displaying the submitted payloadself.
    Otherwise, return a simple JSON object showing the request method.
    """
    if request.method == 'POST':
        return Response({
            "message": "Got a POST request with this data: {}".format(request.data)})
    return Response({"message": "Got a GET request!"})


class FirstClassAPIView(APIView):
    """
    Implement support for GET requests.
    """
    def get(self, request):
        return Response({
            "message": "Got a GET request! This is a class-based APIView."})


class MultiMethodAPIView(APIView):
    """
    Implement support for GET and POST requests.
    """
    def get(self, request):
        return Response({"message": "Got a GET request!"})

    def post(self, request):
        return Response({
            "message": "Got a POST request with this data: {}".format(self.request.data)})


class CustomStatusCode(APIView):
    """
    Return a custom 400 BAD REQUEST status code.
    """
    def get(self, request):
        content = {
            "success": False,
            "msg": "Invalid request, please check the documentation."
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


class CustomHeader(APIView):
    """
    Return a customer `X-RMOTR-IS-AWESOME` response header.
    """
    def get(self, request):
        content = {
            "success": True,
            "msg": "Check the response headers to get a surprise ;-)"
        }
        headers = {
            'X-RMOTR-IS-AWESOME': True
        }
        return Response(content, headers=headers)
