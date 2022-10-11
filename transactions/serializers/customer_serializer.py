from rest_framework import serializers

from transactions import models


class CustomerIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ["id", "name"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ["name"]
