from django.http import Http404,HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

import json

from .models import CarMovements
from rollingstock.models import RailVehicle

def index(request):
    context = {
        "RR_summary": "uello", # TODO: Layout summary
    }
    return render(request, 'genbills/index.html', context)

@csrf_exempt
def generateCarMovement(request):
    # Call the class method to generate a new instance
    new_movement = CarMovements().generate()
    
    # Return the updated list as a JSON response
    return JsonResponse({'car_movements_list': new_movement})

@csrf_exempt
def executeCarMovement(request):
    if request.method == 'POST':
        # send movements to be executed one by one
        data_dict = QueryDict(request.body)
        #print(data_dict)
        for car_id, values in data_dict.items():
            first_four = car_id[:4]
            last_six = car_id[4:10]
            #print(first_four+last_six)
            #print(values)
            destination = values[0]
            # we should probably understand if the car is being loaded or unloaded at this point
            # I'm going to hardcode to always service the car so that the execute function
            # handles this correctly.
            service = True
            #CarMovements.execute(first_four,last_six,source,destination,service)
            vehicle = get_object_or_404(RailVehicle, reporting_mark=first_four,id_number=last_six)
            vehicle.move(destination)
            if service:
                vehicle.service()
            vehicle.save()
    return HttpResponse("Vehicles Moved")