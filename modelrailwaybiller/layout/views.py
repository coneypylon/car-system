from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Layout

@login_required
def layout(request):
    layout_id = request.user.layout_id
    layout = get_object_or_404(Layout, id=layout_id)
    rolling_stock_by_location = layout.list_rolling_stock_by_location()
    locations = list(layout.list_locations().values())
    context = {'rolling_stock_by_location': rolling_stock_by_location, 'locations': locations, 'layout': layout}
    return render(request, 'layout.html', context)
