import sqlite3 as sql
from datetime import datetime
import random

from ..rollingstock.models import RailVehicle
from .models import generate

def main():
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
        cmd = "SELECT * FROM cars c JOIN locations l on c.location=l.id WHERE l.macro_location <> %s AND c.cargo = '%s' AND c.loaded = %s" \
                    % (layout,cargo,loaded)
        cur.execute(cmd)
        raw = cur.fetchall()
        random.shuffle(raw)
        out = []
        for c in raw:
            out.append((c[0],c[1],c[2],c[3],c[4],c[8],c[10]))
        return out

    #def find_off_layout_cars(cargo,loaded,layout):
    #    RailVehicle.#figure this out


    ######################
    #                    #
    # Industrial Demand  #
    #                    #
    ######################

    # Get demands from layout in question
    # might have to make this a global demand calculation
    cur.execute("SELECT * FROM demand d JOIN locations l on d.location=l.id WHERE l.macro_location = %s" % layout)
    potential_demands = cur.fetchall()

    # Calculate cars requested
    demands = []
    for d in potential_demands:
        if d[7][day].lower() == 'y': # the industry requests something today
            if random.random() <= d[4]: # the frequency is met
                numcars = random.randint(d[5],d[6])
                demands.append((d[9],d[1],d[2],numcars))

    ######################
    #                    #
    #       Lifts        #
    #                    #
    ######################

    # Find cars to be picked up
    cur.execute("SELECT * FROM cars c JOIN locations l on c.location=l.id WHERE c.ready_for_pickup = 1 AND l.macro_location = %s" % layout)
    lifts_raw = cur.fetchall()
    lifts = []

    for c in lifts_raw:
        lifts.append((c[0],c[1],c[2],c[3],c[4],c[8],c[10]))

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

    for d in demands:
        rem_dem = d[3] # Remaning Demand - the number of cars remaining for this demand
        for c in lifts:
            if rem_dem > 0 and c[0]+str(c[1]) not in used_cars.keys() and c[3] == d[1] and c[4] == d[2]: # still need cars, car is unused, same cargo and stats
                used_cars[c[0]+str(c[1])] = (c[6],d[0])
                rem_dem -= 1
        # ok, let's grab something off-layout
        pot_cars = find_off_layout_cars(d[1],d[2],layout)
        for c in pot_cars:
            if rem_dem > 0 and c[0]+str(c[1]) not in used_cars.keys() and c[3] == d[1] and c[4] == d[2]: # still need cars, car is unused, same cargo and stats
                used_cars[c[0]+str(c[1])] = (c[6],d[0])
                rem_dem -= 1

    print(used_cars)

    # Calculate trains to be built
    # not sure how to fill trains with stuff not for the layout
    ## From Schedule
    ## Ad-hoc from 

    # Update global state
