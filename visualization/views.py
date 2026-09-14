from django.shortcuts import render
import operator as op

# Create your views here.
def home_page(request):
    scientific_name = "Limosa limosa"
    query = request.POST.get("scientific_name")
    return render(request, "home.html",
                  {"search_results": ([scientific_name] if query is not None and op.contains(scientific_name, query)
    else [])})