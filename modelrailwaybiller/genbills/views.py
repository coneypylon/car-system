from django.http import Http404,HttpResponse, JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import json
import csv

from .models import CarMovements
from rollingstock.models import RailVehicle
from layout.models import Layout

@login_required
def index(request):
    laynum = 1 # gotta change this
    layout = Layout.objects.get(id=laynum)
    cars = layout.list_rolling_stock()
    context = {
        "RR_summary": "There are currently %s cars on the layout, with %s ready to be lifted" % (len(cars),len(cars)),
    }
    return render(request, 'genbills/index.html', context)

new_movement = {}

@csrf_exempt
@login_required
def download_movements(request):
    # Parse the request body based on the content type
    if request.content_type == 'application/json':
        data_dict = json.loads(request.body)
    elif request.content_type == 'application/x-www-form-urlencoded':
        data_dict = QueryDict(request.body.decode('utf-8')).lists()
        data_dict = data_dict = dict((k, v) for k, v in data_dict)
    else:
        # Return an error response if the content type is not supported
        raise NotImplementedError
    # Process the data and create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="movements.csv"'
    writer = csv.writer(response)
    writer.writerow(["Roadname", "ID_number", "Current_Location", "Destination","Destination_ID"])
    for car_id in data_dict.keys():
        values = data_dict[car_id]
        first_four = car_id[17:21]
        last_six = car_id[21:27]
        destination = values[0]
        source = values[1]
        whatever = values[2]
        writer.writerow([first_four,last_six,source,destination,whatever])

    return response

@csrf_exempt
@login_required
def generateCarMovement(request):
    # just global the layout we'll fix it eventually!
    layout = 1
    # we'll let the user pick a date eventually
    date = '1965-01-05'

    # Call the class method to generate a new instance
    new_movement = CarMovements().generate(layout,date)
    
    # Return the updated list as a JSON response
    return JsonResponse({'car_movements_list': new_movement})

@csrf_exempt
@login_required
def executeCarMovement(request):
    if request.method == 'POST':
        # send movements to be executed one by one
        data_dict = QueryDict(request.body)
        print(data_dict)
        for car_id, values in data_dict.items():
            first_four = car_id[:4]
            last_six = car_id[4:10]
            destination = values[0]
            dest_str = data_dict.getlist(car_id)[1]
            # we should probably understand if the car is being loaded or unloaded at this point
            # I'm going to hardcode to always service the car so that the execute function
            # handles this correctly.
            service = True
            #CarMovements.execute(first_four,last_six,source,destination,service)
            vehicle = get_object_or_404(RailVehicle, reporting_mark=first_four,id_number=last_six)
            vehicle.move(destination,dest_str)
            if service:
                vehicle.service()
            vehicle.save()
    return HttpResponse("Vehicles Moved")