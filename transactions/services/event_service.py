from django.http import Http404
from rest_framework import status
from rest_framework.response import Response

from transactions.constants import (
    EVENT_HAS_CUSTOMERS, CUSTOMER_ALREADY_BOOKED_EVENT, CUSTOMER_SUCCESSFULLY_BOOKED_SPACE, EVENT_CANNOT_BOOKED,
    EVENT_HAS_NO_AVAILABLE_SPACES, CUSTOMER_SUCCESSFULLY_REMOVED_SPACE, CUSTOMER_HAS_NO_BOOKED_THIS_EVENT
)
from transactions.models import Event
from transactions.serializers.event_serializer import (
    EventSerializer, EventIDSerializer, EventPublicEventsSerializer, BookEventSerializer
)


class EventService:
    serializer_class = EventSerializer
    serializer_id_class = EventIDSerializer
    serializer_public_event_class = EventPublicEventsSerializer
    serializer_book_event_class = BookEventSerializer
    model = Event

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
        event = self.get_by_id(pk)
        serializer = self.serializer_class(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        event = self.get_by_id(pk)
        if not event.has_customers():
            event.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": EVENT_HAS_CUSTOMERS}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_public_events(self):
        public_events = self.get_queryset().filter(is_public=True)
        serializer = self.serializer_public_event_class(public_events, many=True)
        return Response(serializer.data)

    def book_event(self, pk, request):
        serializer = self.serializer_book_event_class(data=request.data)
        if serializer.is_valid():
            event = self.get_by_id(pk)
            customer = serializer.validated_data["customer"]
            if event.customer_booked_event(customer):
                return Response({"detail": CUSTOMER_ALREADY_BOOKED_EVENT}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if not event.can_event_be_booked():
                return Response({"detail": EVENT_CANNOT_BOOKED}, status=status.HTTP_406_NOT_ACCEPTABLE)
            if not event.get_available_spaces() > 0:
                return Response({"detail": EVENT_HAS_NO_AVAILABLE_SPACES}, status=status.HTTP_406_NOT_ACCEPTABLE)
            event.book_space(customer)
            return Response({"success": CUSTOMER_SUCCESSFULLY_BOOKED_SPACE}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def cancel_booking(self, pk, request):
        serializer = self.serializer_book_event_class(data=request.data)
        if serializer.is_valid():
            event = self.get_by_id(pk)
            customer = serializer.validated_data["customer"]
            if not event.customer_booked_event(customer):
                return Response({"detail": CUSTOMER_HAS_NO_BOOKED_THIS_EVENT}, status=status.HTTP_406_NOT_ACCEPTABLE)
            event.cancel_booking(customer)
            return Response({"success": CUSTOMER_SUCCESSFULLY_REMOVED_SPACE}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

