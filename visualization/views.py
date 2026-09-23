import numpy as np
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import operator as op

from visualization.models import Bird


# Create your views here.
def home_page(request):
    query = request.GET.get("scientific_name")
    return render(request, "home.html",
                  {"search_results": ([bird for bird in Bird.objects.all()
                                       if op.contains(bird.scientific_name.upper(), query.upper())]
                                      if query is not None
                                      else [])})

def distribution(request):
    # Use numpy to easily determine data for bar chart
    property = request.GET.get('property')
    allowlist = ['victory_points', 'wingspan', 'nest_capacity']

    if property is None:
        return HttpResponseBadRequest(f"No property selected.")

    if not property in allowlist:
        return HttpResponseBadRequest("Distribution is not available for selected property.")

    data = np.unique([getattr(bird, property) for bird in Bird.objects.all()],
                               return_counts=True)

    # Convert to a format which JSON parser can understand
    values = [int(v) for v in data[0]]
    counts = [int(c) for c in data[1]]

    return JsonResponse({'distribution': {'values': values, 'counts': counts}})

def stub(request):
    return JsonResponse({})