from rest_framework import status
from rest_framework.response import Response

from transactions.constants import CUSTOMER_HAS_EVENTS
from django.http import Http404
from transactions.models import Customer
from transactions.serializers.customer_serializer import CustomerSerializer, CustomerIDSerializer


class CustomerService:
    serializer_class = CustomerSerializer
    serializer_id_class = CustomerIDSerializer
    model = Customer

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
        customer = self.get_by_id(pk)
        serializer = self.serializer_class(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, pk):
        customer = self.get_by_id(pk)
        if not customer.has_events():
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": CUSTOMER_HAS_EVENTS}, status=status.HTTP_406_NOT_ACCEPTABLE)
