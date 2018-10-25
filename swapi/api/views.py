import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import People, Planet
from api.serializers import PeopleSerializer, PeopleModelSerializer


class PeopleListApiView(APIView):
    def get(self, request):
        raw_people = People.objects.all()
        serial_people = PeopleSerializer(raw_people, many=True)
        return Response(serial_people.data)

    def post(self, request):
        new_person = PeopleSerializer(data=request.data)
        if new_person.is_valid():
            People.objects.create(**new_person.validated_data)
            return Response(f"Thanks for posting {new_person.data}")
        return Response(new_person.errors, status=status.HTTP_400_BAD_REQUEST)


class PeopleDetailApiView(APIView):
    """
    People detail actions. Must support the following method:

        * GET: retrieves information about one particular People object.

        * PUT/PATCH: updates (either fully or partially) a specific People
                     object using submitted payload.

        * DELETE: deletes one particular People object.
    """
    def _get_object(self, people_id):
        return get_object_or_404(People, pk=people_id)

    def get(self, request, people_id):
        one_person = self._get_object(people_id)
        serial_person = PeopleSerializer(one_person)
        return Response(serial_person.data)

    def _update(self, request, people_id, partial=False):
        one_person = self._get_object(people_id)
        serial_person = PeopleSerializer(data=request.data, partial=partial)
        if serial_person.is_valid():
            for field in serial_person.validated_data:
                setattr(one_person, field, serial_person.validated_data[field])
            one_person.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serial_person.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, people_id):
        return self._update(request, people_id)

    def patch(self, request, people_id):
        return self._update(request, people_id, partial=True)

    def delete(self, request, people_id):
        one_person = self._get_object(people_id)
        one_person.delete()
        return Response(status=status.HTTP_200_OK)



class PeopleViewSet(viewsets.ViewSet):
    """
    Implement all required REST actions.

    Follow the default ViewSet method naming convention:
    http://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions

    Use a ModelSerializer instead of a regular Serializer instance.

    Make sure all api.tests still pass.
    """
    
    def _get_object(self, people_id):
        return get_object_or_404(People, pk=people_id)

    def _update(self, request, people_id, partial=False):
        one_person = self._get_object(people_id)
        serial_person = PeopleModelSerializer(data=request.data, partial=partial)
        if serial_person.is_valid():
            for field in serial_person.validated_data:
                setattr(one_person, field, serial_person.validated_data[field])
            one_person.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serial_person.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(sef, request):
        raw_people = People.objects.all()
        serial_people = PeopleModelSerializer(raw_people, many=True)
        return Response(serial_people.data)

    def create(self, request):
        new_person = PeopleModelSerializer(data=request.data)
        if new_person.is_valid():
            People.objects.create(**new_person.validated_data)
            return Response(f"Thanks for posting {new_person.data}")
        return Response(new_person.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        one_person = self._get_object(pk)
        serial_person = PeopleModelSerializer(one_person)
        return Response(serial_person.data)

    def update(self, request, pk=None):
        return self._update(request, pk)

    def partial_update(self, request, pk=None):
        return self._update(request, pk, partial=True)

    def destroy(self, request, pk=None):
        one_person = self._get_object(pk)
        one_person.delete()
        return Response(status=status.HTTP_200_OK)


class PeopleModelViewSet(viewsets.ModelViewSet):
    """
    Migrate the same logic as above, but using ModelViewSets
    and ModelSerializers.

    Make sure all api.tests still pass.
    """
    serializer_class = PeopleModelSerializer
    queryset = People.objects.all()
