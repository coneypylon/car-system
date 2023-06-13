import datetime

import sqlite3 as sql
from datetime import datetime
import random

from rollingstock.models import RailVehicle
from layout.models import Layout,Location,Demand

from django.db import models
from django.utils import timezone

class CarMovements(models.Model):
    state_id = models.PositiveIntegerField()

    def generate(self, layout_id, date):
        layout = Layout.objects.get(id=layout_id)
        day = int(datetime.strptime(date, "%Y-%m-%d").strftime('%w'))
        used_cars = {}

        demands = Demand.objects.filter(layout=layout_id, days__contains=day)

        # Retrieve rail vehicles associated with the desired layout
        layout_location_ids = Location.objects.filter(layout__id=layout_id).values_list('id', flat=True)
        lifts = RailVehicle.objects.filter(ready_for_pickup=True, location__in=layout_location_ids)

        for demand in demands:
            remaining_demand = demand.num_cars
            for car in lifts:
                if remaining_demand > 0 and car.reporting_mark + str(car.id_number) not in used_cars.keys() and car.cargo == demand.cargo and car.is_loaded == demand.loaded:
                    used_cars[car.reporting_mark + str(car.id_number)] = (car.location_str, demand.name, demand.id)
                    remaining_demand -= 1

        for car in lifts:
            if car.reporting_mark + str(car.id_number) not in used_cars.keys():
                destination, destination_id = layout.find_destination_for_cargo(car.cargo)
                used_cars[car.reporting_mark + str(car.id_number)] = (car.location, destination, destination_id)

        return used_cars


