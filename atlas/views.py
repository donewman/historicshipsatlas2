from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.base import RedirectView
from django.core import serializers
from django.contrib.postgres.search import SearchVector
from atlas.models import Ship, Type, City, Country, Status, Use, Owner
from atlas.forms import BasicSearchForm

# Index view
def index(request):
    # Serializes static ships, i.e. ships without FleetMon IDs, to JSON
    static_ships_json = serializers.serialize('json', Ship.objects.all().filter(fleetmon__isnull=True), fields=('name', 'type', 'year_built', 'city', 'country', 'status', 'lat', 'lon', 'slug'), use_natural_foreign_keys=True)
    # Serializes active ships, i.e. ships with FleetMon IDs, to JSON
    active_ships_json = serializers.serialize('json', Ship.objects.all().filter(fleetmon__isnull=False), fields=('name', 'fleetmon', 'type', 'year_built', 'slug'), use_natural_foreign_keys=True)
    # Passes both JSON objects as context
    context = {'static_ships_json': static_ships_json, 'active_ships_json': active_ships_json,}

    return render(request, 'index.html', context,)

# List of all ships
class ShipListView(ListView):
    model = Ship

# Basic search form
class SearchView(ListView):
    model = Ship
    def get_queryset(self):
        try:
            search_string = self.request.GET["keywords"]
            results = Ship.objects.annotate(
                search=(
                    SearchVector("name", "type__name", "city__name", "city__region", "country__name", "status__name", "uses__name", "owner__name", "former_names", "description")
                ),
            ).filter(search=search_string).distinct("pk")
            return results
        except KeyError:
            return Ship.objects.none()

# Details view for ships
class ShipDetailView(DetailView):
    model = Ship

# Details view for types of ships
class TypeDetailView(DetailView):
    model = Type

# Details view for cities
class CityDetailView(DetailView):
    model = City

# Details view for countries
class CountryDetailView(DetailView):
    model = Country

# Details view for statuses
class StatusDetailView(DetailView):
    model = Status

# Details view for uses
class UseDetailView(DetailView):
    model = Use

# Details view for owners
class OwnerDetailView(DetailView):
    model = Owner
