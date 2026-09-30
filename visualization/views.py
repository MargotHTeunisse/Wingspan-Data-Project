import operator as op

from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from rest_framework import generics

from visualization.models import Bird
from visualization.serializers import BirdSerializer


# Create your views here.
def home_page(request):
    # Use helper function within homepage to apply filter in accordance with user preferences
    def filter_applies(bird: Bird) -> bool:
        # Pass bird through habitat filter
        if request.GET.get("forest") == 'on' and not bird.lives_in_forest:
            return False
        if request.GET.get("grasslands") == 'on' and not bird.lives_in_grasslands:
            return False
        if request.GET.get("wetlands") == 'on' and not bird.lives_in_wetlands:
            return False

        return True

    query = request.GET.get("scientific_name")

    return render(request, "home.html",
                  {"search_results": ([bird for bird in Bird.objects.all()
                                       if op.contains(bird.scientific_name.upper(), query.upper())
                                       and filter_applies(bird)]
                                      if query is not None
                                      else [])})

class BirdList(generics.ListCreateAPIView):
    queryset = Bird.objects.all()
    serializer_class = BirdSerializer

def distribution(request):
    # Use numpy to easily determine data for bar chart
    bird_property = request.GET.get('property')
    allowlist = ['victory_points', 'wingspan', 'nest_capacity', 'nest_type']

    if bird_property is None:
        return HttpResponseBadRequest(f"No property selected.")

    if not bird_property in allowlist:
        return HttpResponseBadRequest("Distribution is not available for selected property.")

    data = [getattr(bird, bird_property) for bird in Bird.objects.all()
            if getattr(bird, bird_property) is not None]

    # Convert to a format which JSON parser can understand
    values = list(set(data))
    values.sort()
    counts = [data.count(val) for val in values]

    return JsonResponse({'distribution': {'values': values, 'counts': counts}})

def stub(request):
    return JsonResponse({})