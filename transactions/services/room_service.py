from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

from transactions.constants import ROOM_HAS_EVENTS
from transactions.models import Room
from transactions.serializers.room_serializer import RoomSerializer, RoomIDSerializer


class RoomService:
    serializer_class = RoomSerializer
    serializer_id_class = RoomIDSerializer
    model = Room

    def get_queryset(self):
        return self.model.objects.all()

    def get_by_id(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, pk):
        if pk:
            serializer = self.serializer_id_class(self.get_by_id(pk))
        else:
            serializer = self.serializer_id_class(self.get_queryset(), many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, pk, request):
        room = self.get_by_id(pk)
        serializer = self.serializer_class(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        room = self.get_by_id(pk)
        if not room.has_events():
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": ROOM_HAS_EVENTS}, status=status.HTTP_406_NOT_ACCEPTABLE)
