from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    query = request.POST.get("scientific_name")
    return render(request, "home.html",
                  {"search_results": ([] if query is None else [query])})