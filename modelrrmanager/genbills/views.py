from django.http import Http404,HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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