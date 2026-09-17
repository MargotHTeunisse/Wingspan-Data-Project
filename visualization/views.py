from django.shortcuts import render
import operator as op

from visualization.models import Bird


# Create your views here.
def home_page(request):
    query = request.POST.get("scientific_name")
    return render(request, "home.html",
                  {"search_results": ([bird.scientific_name for bird in Bird.objects.all()
                                       if op.contains(bird.scientific_name, query)] if query is not None
                                      else [])})