from rest_framework import views

from transactions.services.customer_service import CustomerService


class CustomerAPIView(views.APIView):
    service = CustomerService()

    def get(self, request, pk=None, *args, **kwargs):
        return self.service.get(pk)

    def post(self, request, *args, **kwargs):
        return self.service.create(request)

    def put(self, request, pk, *args, **kwargs):
        return self.service.update(pk, request)

    def delete(self, request, pk, *args, **kwargs):
        return self.service.delete(pk)
