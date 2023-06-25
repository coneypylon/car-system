from django.http import Http404,HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from layout.models import Layout

from .forms import StockForm, ConfirmationForm
from .models import RailVehicle
#from modelrrmanager.locations.models import Location

@login_required
def index(request):
    # load up some context
    layouts = Layout.objects.filter(owner_id=request.user.id)
    locations = []
    for layout in layouts:
        locations.extend(list(layout.list_locations().values()))
    # receive da form
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            newstock = form.save(commit=False)
            newstock.location_str = 'Unknown'
            newstock.last_loaded_unloaded = newstock.location
            newstock.ready_for_pickup = True
            for location in locations:
                if location['id'] == newstock.location:
                    newstock.location_str = location['name']
            newstock.save()
            return HttpResponse("Stock Received!")
        
    else:
        form = StockForm()
    
    road_listed_vehicles = RailVehicle.objects.order_by('reporting_mark','id_number') # this is every vehicle - limit to whatever the user owns eventually.
    #output = ', '.join(str(q) for q in road_listed_vehicles)
    #template = loader.get_template('rollingstock/index.html')
    context = {
        'road_listed_vehicles': road_listed_vehicles,
        'form': form,
        'locations':locations,
    }
    #return HttpResponse(template.render(context,request))
    return render(request, 'rollingstock/index.html', context)


@csrf_exempt
@login_required
def detail(request, r_stock_id):
    try: 
        vehicle = RailVehicle.objects.get(pk=r_stock_id)
        if request.method == "POST":
            form = ConfirmationForm(request.POST)
            if form.is_valid() and form.cleaned_data['registration'] == vehicle.reporting_mark + str(vehicle.id_number):
                vehicle.delete()
                return HttpResponse("Stock Deleted!")
        else:
            form = ConfirmationForm()
        location = str(vehicle.location_str)
        context = {
            "form": form,
            'vehicle':vehicle,
            'location':location,
        }
        return render(request, 'rollingstock/detail.html',context)
    except RailVehicle.DoesNotExist:
        raise Http404("Vehicle does not exist!")

