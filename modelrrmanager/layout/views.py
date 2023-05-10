from django.shortcuts import render, get_object_or_404
from .models import Layout

def layout(request):
    laynum = 1 # gotta change this
    layout = Layout.objects.get(id=laynum)
    rolling_stock_by_location = layout.ListRollingStockByLocation()
    locations = list(layout.ListLocations().values())
    context = {'rolling_stock_by_location': rolling_stock_by_location, 'locations': locations, 'layout':layout}
    return render(request, 'layout.html', context)