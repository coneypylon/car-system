from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Layout, Location
from .forms import LayoutForm, LocationForm

@login_required
def layout(request):
    if request.method == 'GET':
        layout_id = request.user.layout_id
        layout = get_object_or_404(Layout, id=layout_id)
        rolling_stock_by_location = layout.list_rolling_stock_by_location()
        locations = list(layout.list_locations().values())
        form = LocationForm()
        context = {
            'rolling_stock_by_location': rolling_stock_by_location,
            'locations': locations, 
            'layout': layout,
            'form': form
            }
        return render(request, 'layout.html', context)
    elif request.method == 'POST':
        # let's make a layout!
        form = LayoutForm(request.POST)
        if form.is_valid():
            newlayout = form.save(commit=False)
            try:
                curmaxid = Layout.objects.latest('id').id
            except:
                curmaxid = 0
            if request.user.layout_id > curmaxid:
                newlayout.id = request.user.layout_id
            else:
                newlayout.id = curmaxid + 1
                # and we need to implement an update to the user...
            newlayout.save()

@login_required
def location(request):
    if request.method == 'POST':
        # let's make a location
        layout_id = request.user.layout_id
        layout = get_object_or_404(Layout, id=layout_id)
        form = LocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            new_location = Location.objects.create(name=name, description=description,macro_location=layout_id)
            layout.locations.add(new_location)
            return HttpResponse("Location Received!")
    if request.method == 'GET':
        response = redirect('layout')
        return response
