from rest_framework import views
from transactions.services.room_service import RoomService


class RoomAPIView(views.APIView):
    service = RoomService()

    def get(self, request, pk=None, *args, **kwargs):
        return self.service.get(pk)

    def post(self, request, *args, **kwargs):
        return self.service.create(request)

    def put(self, request, pk, *args, **kwargs):
        return self.service.update(pk, request)

    def delete(self, request, pk, *args, **kwargs):
        return self.service.delete(pk)
