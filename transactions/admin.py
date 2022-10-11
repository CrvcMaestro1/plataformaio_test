from django.contrib import admin

from transactions.models import Room, Customer, Event

admin.site.register(Room)
admin.site.register(Customer)
admin.site.register(Event)
