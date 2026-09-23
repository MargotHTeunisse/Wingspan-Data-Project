import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
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

def victory_points_distribution(request):
    # Use numpy to easily determine data for bar chart
    data = np.unique([bird.victory_points for bird in Bird.objects.all()],
                               return_counts=True)

    # Convert to a format which JSON parser can understand
    values = [int(v) for v in data[0]]
    counts = [int(c) for c in data[1]]

    return JsonResponse({'distribution': {'values': values, 'counts': counts}})

def wingspan_distribution(request):
    data = np.unique([bird.wingspan for bird in Bird.objects.all()],
                               return_counts=True)

    # Convert to a format which JSON parser can understand
    values = [int(v) for v in data[0]]
    counts = [int(c) for c in data[1]]

    return JsonResponse({'distribution': {'values': values, 'counts': counts}})

def nest_capacity_distribution(request):
    data = np.unique([bird.nest_capacity for bird in Bird.objects.all()],
                               return_counts=True)

    # Convert to a format which JSON parser can understand
    values = [int(v) for v in data[0]]
    counts = [int(c) for c in data[1]]

    return JsonResponse({'distribution': {'values': values, 'counts': counts}})

def stub(request):
    return JsonResponse({})