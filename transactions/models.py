from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_capacity(value):
    if value < 1:
        raise ValidationError(
            _('Room at least needs 1 space.'),
        )


class ParentModel(models.Model):
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.status = True
        models.Model.save(self)

    def delete(self, *args, **kwargs):
        self.status = False
        models.Model.save(self)

    class Meta:
        abstract = True


class StatusManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Room(ParentModel):
    name = models.CharField(verbose_name="Name", max_length=25)
    capacity = models.IntegerField(verbose_name="Capacity", validators=[validate_capacity])

    objects = StatusManager()

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}, Capacity: {self.capacity}"

    def has_events(self):
        return self.event_set.all().count() > 0

    def already_has_events_in_day(self, day):
        return self.event_set.filter(day=day).exclude(pk=self.pk).count() > 0


class Customer(ParentModel):
    name = models.CharField(verbose_name="Name", max_length=50)

    objects = StatusManager()

    def __str__(self):
        return f"ID: {self.id}, Name: {self.name}"

    def has_events(self):
        return self.event_set.all().count() > 0


class Event(ParentModel):
    room = models.ForeignKey(Room, on_delete=models.PROTECT)
    day = models.DateField(verbose_name="Event Day")
    name = models.CharField(verbose_name="Name", max_length=100)
    is_public = models.BooleanField()
    customers = models.ManyToManyField(Customer)

    objects = StatusManager()

    def __str__(self):
        return f"ID: {self.id}, Room: {self.room.id}, Name: {self.name}, Is Public?: {self.is_public}"

    def has_customers(self):
        return self.customers.all().count() > 0

    def get_available_spaces(self):
        booked_customers = self.customers.all().count()
        return self.room.capacity - booked_customers

    def customer_booked_event(self, customer):
        return self.customers.filter(id=customer.id).exists()

    def can_event_be_booked(self):
        return self.is_public

    def book_space(self, customer):
        self.customers.add(customer)

    def cancel_booking(self, customer):
        self.customers.remove(customer)
