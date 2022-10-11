from rest_framework import serializers

from transactions import models


class RoomIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ["id", "name", "capacity"]


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ["name", "capacity"]
