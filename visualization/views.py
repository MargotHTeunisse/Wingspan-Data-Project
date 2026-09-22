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

def stub(request):
    return JsonResponse({})