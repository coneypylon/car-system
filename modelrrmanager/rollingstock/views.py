from django.http import Http404,HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import RailVehicle
#from modelrrmanager.locations.models import Location

def index(request):
    road_listed_vehicles = RailVehicle.objects.order_by('reporting_mark','id_number')
    #output = ', '.join(str(q) for q in road_listed_vehicles)
    #template = loader.get_template('rollingstock/index.html')
    context = {
        'road_listed_vehicles': road_listed_vehicles,
    }
    #return HttpResponse(template.render(context,request))
    return render(request, 'rollingstock/index.html', context)

def detail(request, r_stock_id):
    try: 
        vehicle = RailVehicle.objects.get(pk=r_stock_id)
        try:
            location = Location.objects.get(pk=vehicle.location)
        except:
            location = str(vehicle.location)
    except RailVehicle.DoesNotExist:
        raise Http404("Vehicle does not exist!")
    return render(request, 'rollingstock/detail.html',{'vehicle':vehicle,'location':location})

