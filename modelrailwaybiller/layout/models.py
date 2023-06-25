from django.db import models
from rollingstock.models import RailVehicle
import random
from django.conf import settings

class Location(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    macro_location = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.description}"

class Layout(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    locations = models.ManyToManyField(Location)

    def list_locations(self):
        return self.locations.all()

    def list_rolling_stock(self):
        return RailVehicle.objects.filter(location__in=self.locations.all())

    def list_rolling_stock_by_location(self):
        rolling_stock_by_location = {}
        for location in self.locations.all():
            rolling_stock_by_location[location.id] = list(RailVehicle.objects.filter(location=location.id))
        return rolling_stock_by_location
    
    def find_destination_for_cargo(self, cargo, loaded,day):
        layout_id = self.id
        demands = Demand.objects.filter(layout_id=layout_id, cargo=cargo, loaded=loaded)
        valid_demands = []
        for demand in demands:
            if demand.days[day].lower() == 'y' and random.random() <= demand.frequency:
                valid_demands.append((demand.name, demand.id))

        random.shuffle(valid_demands)
        return valid_demands[0] if valid_demands else None
    
    def find_global_destination_for_cargo(self, cargo, loaded,day):
        layout_id = self.id
        demands = Demand.objects.filter(cargo=cargo, loaded=loaded)
        valid_demands = []

        for demand in demands:
            if demand.days[day].lower() == 'y' and random.random() <= demand.frequency:
                valid_demands.append((demand.name, demand.id))

        random.shuffle(valid_demands)
        return valid_demands[0] if valid_demands else None

class Demand(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=32)
    loaded = models.BooleanField()
    min_cars = models.PositiveIntegerField()
    max_cars = models.PositiveIntegerField()
    frequency = models.FloatField()
    name = models.CharField(max_length=32)
    days = models.CharField(max_length=7)
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE)

    def __str__(self):
        return self.name