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

        # Retrieve rail vehicles associated with the desired layout
        layout_location_ids = Location.objects.filter(layout__id=layout_id).values_list('id', flat=True)
        lifts = RailVehicle.objects.filter(ready_for_pickup=True, location__in=layout_location_ids)

        # Retrieve rail vehicles not associated with the desired layout
        offlayout_location_ids = Location.objects.exclude(layout__id=layout_id).values_list('id', flat=True)
        dropoffs = RailVehicle.objects.filter(ready_for_pickup=True, location__in=offlayout_location_ids)

        for car in lifts:
            if car.reporting_mark + str(car.id_number) not in used_cars.keys():
                try:
                    destination, destination_id = layout.find_destination_for_cargo(car.cargo,car.loaded,day)
                    used_cars[car.reporting_mark + str(car.id_number)] = (car.location_str, destination, destination_id)
                except TypeError:
                    try:
                        destination, destination_id = layout.find_global_destination_for_cargo(car.cargo,car.loaded,day)
                        used_cars[car.reporting_mark + str(car.id_number)] = (car.location_str, destination, destination_id)
                    except TypeError:
                        pass
        

        for car in dropoffs:
            if car.reporting_mark + str(car.id_number) not in used_cars.keys():
                try:
                    destination, destination_id = layout.find_destination_for_cargo(car.cargo,car.loaded,day)
                    used_cars[car.reporting_mark + str(car.id_number)] = (car.location_str, destination, destination_id)
                except TypeError:
                    try:
                        destination, destination_id = layout.find_global_destination_for_cargo(car.cargo,car.loaded,day)
                        used_cars[car.reporting_mark + str(car.id_number)] = (car.location_str, destination, destination_id)
                    except TypeError:
                        pass

        return used_cars


