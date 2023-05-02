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
    
    def ListLocations(self):
        cur = connection(global_db)
        cur.execute("SELECT id, name, description, macro_location FROM locations WHERE macro_location = %s" % self.id)
        locations = {}
        for location in cur.fetchall():
            locations[location[0]] = Location(location[0],location[1],location[2],location[3])
        return locations 
    
    def ListRollingStock(self):
        possible_locations = self.ListLocations()
        allVehicles = RailVehicle.objects.filter(location__in=possible_locations.keys())
        return allVehicles