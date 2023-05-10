from django.db import models

import sqlite3

from django.db import models
from django.utils import timezone

from rollingstock.models import RailVehicle

global_db = 'KitchenerSub.db' # this needs to go

def connection(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    return cur

class Location:
    def __init__(self,id,name,description,macro_location):
        self.id = id
        self.name = name
        self.description = description
        self.macro_location = macro_location
    def __str__(self):
        return "%s - %s" % (self.name,self.description)

class Layout(models.Model):
    id = models.CharField(max_length=12,primary_key=True)
    name = models.CharField(max_length=32)
    locations = {}
    
    def ListLocations(self):
        cur = connection(global_db)
        cur.execute("SELECT id, name, description, macro_location FROM locations WHERE macro_location = %s" % self.id)
        locations = {}
        for location in cur.fetchall():
            locations[location[0]] = Location(location[0],location[1],location[2],location[3])
        return locations
    
    def ListRollingStock(self):
        possible_locations = self.ListLocations()
        lst_of_keys = list(possible_locations.keys())
        allVehicles = RailVehicle.objects.filter(location__in=lst_of_keys)
        return list(allVehicles)
    
    def ListRollingStockByLocation(self):
        possible_locations = self.ListLocations()
        rolling_stock_by_location = {}
        for location_id in possible_locations:
            rolling_stock_by_location[location_id] = list(RailVehicle.objects.filter(location=location_id))
        return rolling_stock_by_location