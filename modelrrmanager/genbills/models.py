import datetime

import sqlite3 as sql
from datetime import datetime
import random

from rollingstock.models import RailVehicle

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class CarMovements(models.Model):
    state_id = models.PositiveIntegerField()
    

    def generate(self):
        print("hello")
        # Constants - we'll eventually need to get these from the user
        db = "KitchenerSub.db"
        layout = 1
        date = "1995-07-05" # a Wednesday

        # SQL setup
        con = sql.connect(db)
        cur = con.cursor()

        # Convert some formats
        day = int(datetime.strptime(date,"%Y-%m-%d").strftime('%w'))

        # Helper Functions
        def boolconv(val):
            if val:
                return 1
            else:
                return 

        def find_off_layout_cars(cargo,loaded,layout):
            '''cmd = "SELECT * FROM cars c JOIN locations l on c.location=l.id WHERE l.macro_location <> %s AND c.cargo = '%s' AND c.loaded = %s" \
                        % (layout,cargo,loaded)
            cur.execute(cmd)
            raw_list_of_cars = cur.fetchall()
            random.shuffle(raw_list_of_cars)
            out = []
            for car in raw_list_of_cars:
                print(car)
                out.append((car[0],car[1],car[2],car[3],car[4],car[8],car[10])) 
                # ^ reporting mark, id #, AAR type, cargo, Loaded (Bool), Image URL, Current Location String
            return out'''
            return find_cars(cargo=cargo,loaded=loaded,layout=layout,offlayout=True)
        
        def find_cars(cargo='',loaded='',layout=1,offlayout=True,lifts=False):
            if offlayout:
                cmd = "SELECT * FROM rollingstock_railvehicle c JOIN locations l on c.location=l.id WHERE l.macro_location <> %s AND c.cargo = '%s' AND c.loaded = %s" \
                        % (layout,cargo,loaded)
            elif lifts:
                cmd = "SELECT * FROM rollingstock_railvehicle c JOIN locations l on c.location=l.id WHERE c.ready_for_pickup = 1 AND l.macro_location = %s" % layout
            cur.execute(cmd)
            raw_list_of_cars = cur.fetchall()
            random.shuffle(raw_list_of_cars)
            carAttributes = ["id","reportingMark", "aarType", "cargo", "isLoaded", "locationID","lastServicedLocation",
                             "isReady", "imageURL","idNumber", "locationID2", "locationStr","locationDescription","macroLocationID"]
            out = []
            for aCar in raw_list_of_cars:
                readableDict = {}
                for x in range(0, len(carAttributes)-1):
                    readableDict[carAttributes[x]] = aCar[x]
                out.append(readableDict)
            return out
        
        def findDestinationForCargo(cargo,layout,offlayout=True):
            if offlayout:
                cmd = "SELECT * FROM demand d JOIN locations l on d.location=l.id WHERE l.macro_location %s %s AND d.cargo = '%s'" % ("<>", layout, cargo)
            else:
                cmd = "SELECT * FROM demand d JOIN locations l on d.location=l.id WHERE l.macro_location %s %s AND d.cargo = '%s'" % ("=", layout, cargo)
            print(cmd)
            cur.execute(cmd)
            potential_demands = cur.fetchall()
            demands = []
            for demand in potential_demands:
                if demand[7][day].lower() == 'y': # the industry requests something today
                    if random.random() <= demand[4]: # the frequency is met
                        demands.append((demand[9],demand[0]))
            random.shuffle(demands)
            return demands[0]


        #def find_off_layout_cars(cargo,loaded,layout):
        #    RailVehicle.#figure this out


        ######################
        #                    #
        # Industrial Demand  #
        #                    #
        ######################

        # Get demands from layout in question
        # might have to make this a global demand calculation
        cmd = "SELECT * FROM demand d JOIN locations l on d.location=l.id WHERE l.macro_location = %s" % layout
        cur.execute(cmd)
        potential_demands = cur.fetchall()

        # Calculate cars requested
        demands = []
        for demand in potential_demands:
            if demand[7][day].lower() == 'y': # the industry requests something today
                if random.random() <= demand[4]: # the frequency is met
                    numcars = random.randint(demand[5],demand[6])
                    demands.append((demand[9],demand[1],demand[2],numcars,demand[0]))

        ######################
        #                    #
        #       Lifts        #
        #                    #
        ######################

        # Find cars to be picked up
        #cur.execute("SELECT * FROM cars c JOIN locations l on c.location=l.id WHERE c.ready_for_pickup = 1 AND l.macro_location = %s" % layout)
        #lifts_raw = cur.fetchall()
        lifts = find_cars(layout=layout,lifts=True,offlayout=False)

        #for car in lifts_raw:
        #    lifts.append((car[0],car[1],car[2],car[3],car[4],car[8],car[10]))
            # ^ reporting mark, id #, AAR type, cargo, Loaded (Bool), Image URL, Current Location String

        ######################
        #                    #
        #   Build Trains     #
        #                    #
        ######################

        used_cars = dict()

        # Find cars for requests & destinations for cars on-layout
        # eventually this will be global
        on_layout_moves = []
        off_layout_moves = []

        for demand in demands: # demand = Name, cargo, want loaded, number of cars, LocationID
            rem_dem = demand[3] # Remaning Demand - the number of cars remaining for this demand
            for car in lifts:
                if rem_dem > 0 and car["reportingMark"]+str(car["idNumber"]) not in used_cars.keys() and car["cargo"] == demand[1] and car["isLoaded"] == demand[2]: # still need cars, car is unused, same cargo and stats
                    used_cars[car["reportingMark"]+str(car["idNumber"])] = (car["locationStr"],demand[0],demand[4])
                    rem_dem -= 1
            # ok, let's grab something off-layout
            pot_cars = find_off_layout_cars(demand[1],demand[2],layout)
            for car in pot_cars:
                if rem_dem > 0 and car["reportingMark"]+str(car["idNumber"]) not in used_cars.keys() and car["cargo"] == demand[1] and car["isLoaded"] == demand[2]: # still need cars, car is unused, same cargo and stats
                    used_cars[car["reportingMark"]+str(car["idNumber"])] = (car["locationStr"],demand[0],demand[4])
                    rem_dem -= 1

        for car in lifts:
            if car["reportingMark"]+str(car["idNumber"]) not in used_cars.keys():
                destination, destination_id = findDestinationForCargo(car["cargo"],layout)
                used_cars[car["reportingMark"]+str(car["idNumber"])] = (car["locationStr"],destination,destination_id)

        return used_cars

        # Calculate trains to be built
        # not sure how to fill trains with stuff not for the layout
        ## From Schedule
        ## Ad-hoc from 

        # Update global state
