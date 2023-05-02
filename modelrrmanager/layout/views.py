from django.shortcuts import render, get_object_or_404
from .models import Layout

def layout(request):
    laynum = "1" # gotta change this
    layout = Layout.objects.get(id=laynum)
    rolling_stock = layout.ListRollingStock()
    print(rolling_stock)
    locations = layout.ListLocations()
    print(locations)
    context = {'rolling_stock': rolling_stock, 'locations': locations}
    return render(request, 'layout.html', context)