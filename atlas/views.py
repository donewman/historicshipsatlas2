from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import RedirectView
from django.core import serializers
from django.contrib.postgres.search import SearchVector
from atlas.models import Ship, Type, City, Country, Status, Use, Owner
from atlas.forms import SearchForm

# Index view
def index(request):
    # Serializes static ships, i.e. ships without FleetMon IDs, to JSON
    static_ships_json = serializers.serialize('json', Ship.objects.all().filter(fleetmon__isnull=True), fields=('name', 'type', 'year_built', 'city', 'country', 'status', 'lat', 'lon', 'slug'), use_natural_foreign_keys=True)
    # Serializes active ships, i.e. ships with FleetMon IDs, to JSON
    active_ships_json = serializers.serialize('json', Ship.objects.all().filter(fleetmon__isnull=False), fields=('name', 'fleetmon', 'type', 'year_built', 'slug'), use_natural_foreign_keys=True)
    # Passes both JSON objects as context
    context = {'static_ships_json': static_ships_json, 'active_ships_json': active_ships_json,}

    return render(request, 'index.html', context,)

# Advanced search form
class AdvancedSearchView(FormView):
    template_name = 'advanced_search.html'
    form_class = SearchForm
    success_url = '/atlas/search/'

# Search results
class SearchResultsView(ListView):
    template_name = 'search_results.html'
    model = Ship

    def get_queryset(self):
        qs = Ship.objects.all()
        if self.request.GET['keywords']:
            qs = qs.annotate(
                search=(
                        SearchVector('name', 'type__name', 'city__name', 'city__region', 'country__name', 'status__name', 'uses__name', 'owner__name', 'former_names', 'description')
                    ),).filter(search=self.request.GET['keywords']).distinct('pk')
        if self.request.GET.get('name'):
            qs = qs.annotate(search=(SearchVector('name')),).filter(search=self.request.GET['name']).distinct('pk')
        if self.request.GET.get('imo'):
            qs = qs.filter(imo__exact=self.request.GET['imo'])
        if self.request.GET.get('type'):
            qs = qs.filter(type=self.request.GET['type'])
        if self.request.GET.get('year_built_from'):
            qs = qs.filter(year_built__gte=self.request.GET['year_built_from'])
        if self.request.GET.get('year_built_to'):
            qs = qs.filter(year_built__lte=self.request.GET['year_built_to'])
        if self.request.GET.get('tonnage_from'):
            qs = qs.filter(tonnage__gte=self.request.GET['tonnage_from'])
        if self.request.GET.get('tonnage_to'):
            qs = qs.filter(tonnage__lte=self.request.GET['tonnage_to'])
        if self.request.GET.get('length_from'):
            qs = qs.filter(length__gte=self.request.GET['length_from'])
        if self.request.GET.get('length_to'):
            qs = qs.filter(length__lte=self.request.GET['length_to'])
        if self.request.GET.get('beam_from'):
            qs = qs.filter(beam__gte=self.request.GET['beam_from'])
        if self.request.GET.get('beam_to'):
            qs = qs.filter(beam__lte=self.request.GET['beam_to'])
        if self.request.GET.get('city'):
            qs = qs.annotate(search=(SearchVector('city__name', 'city__region')),).filter(search=self.request.GET['city']).distinct('pk')
        if self.request.GET.get('country'):
            qs = qs.filter(country=self.request.GET['country'])
        if self.request.GET.get('status'):
            qs = qs.filter(status=self.request.GET['status'])
        if self.request.GET.get('uses'):
            qs = qs.filter(uses=self.request.GET['uses'])
        if self.request.GET.get('owner'):
            qs = qs.annotate(search=(SearchVector('owner__name')),).filter(search=self.request.GET['owner']).distinct('pk')
        if self.request.GET.get('former_names'):
            qs = qs.annotate(search=(SearchVector('former_names')),).filter(search=self.request.GET['former_names']).distinct('pk')
        return qs.order_by('name')

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
