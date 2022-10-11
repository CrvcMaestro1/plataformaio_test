from rest_framework import views

from transactions.services.event_service import EventService


class EventAPIView(views.APIView):
    service = EventService()

    def get(self, request, pk=None, *args, **kwargs):
        return self.service.get(pk)

    def post(self, request, *args, **kwargs):
        return self.service.create(request)

    def put(self, request, pk, *args, **kwargs):
        return self.service.update(pk, request)

    def delete(self, request, pk, *args, **kwargs):
        return self.service.delete(pk)


class EventPublicAPIView(views.APIView):
    service = EventService()

    def get(self, request, *args, **kwargs):
        return self.service.get_public_events()


class BookEventAPIView(views.APIView):
    service = EventService()

    def post(self, request, pk, *args, **kwargs):
        return self.service.book_event(pk, request)


class CancelBookingAPIView(views.APIView):
    service = EventService()

    def post(self, request, pk, *args, **kwargs):
        return self.service.cancel_booking(pk, request)
