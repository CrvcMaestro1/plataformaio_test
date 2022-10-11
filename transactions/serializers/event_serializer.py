from rest_framework import serializers

from transactions import models
from transactions.constants import ROOM_HAS_EVENTS_THIS_DAY
from transactions.serializers.customer_serializer import CustomerSerializer
from transactions.serializers.room_serializer import RoomSerializer


class EventIDSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    customers = CustomerSerializer(many=True)

    class Meta:
        model = models.Event
        fields = ["id", "room", "day", "name", "is_public", "customers"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["room", "day", "name", "is_public"]

    def validate(self, attrs):
        room = attrs['room']
        day = attrs['day']
        if room.already_has_events_in_day(day):
            raise serializers.ValidationError({"room": ROOM_HAS_EVENTS_THIS_DAY})
        return attrs


class EventPublicEventsSerializer(serializers.ModelSerializer):
    room = RoomSerializer()
    available_spaces = serializers.SerializerMethodField()

    class Meta:
        model = models.Event
        fields = ["id", "room", "day", "name", "is_public", "available_spaces"]

    def get_available_spaces(self, obj):
        return obj.get_available_spaces()


class BookEventSerializer(serializers.Serializer):
    customer = serializers.PrimaryKeyRelatedField(required=True, queryset=models.Customer.objects.all())

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
