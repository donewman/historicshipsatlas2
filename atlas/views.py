from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView
from django.views.generic.base import RedirectView
from django.core import serializers
from django.contrib.postgres.search import SearchVector
from atlas.models import Ship, Type, City, Country, Status, Use, Owner
from atlas.forms import SearchForm

# Index view
def index(request):
    # Serializes static ships to JSON
    static_ships_json = serializers.serialize('json', Ship.objects.all().filter(active=False), fields=('name', 'type', 'year_built', 'city', 'country', 'status', 'lat', 'lon', 'slug'), use_natural_foreign_keys=True)
    # Passes static ships as context
    context = {'static_ships_json': static_ships_json,}

    return render(request, 'index.html', context,)

# Advanced search form
class AdvancedSearchView(FormView):
    template_name = 'advanced_search.html'
    form_class = SearchForm
    success_url = '/atlas/search/'

# Search results
class SearchResultsView(ListView):
    template_name = 'search_results.html'
    form_class = SearchForm
    model = Ship

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        qs = Ship.objects.all()
        if form.is_valid():
            if form.cleaned_data['keywords']:
                qs = qs.annotate(
                    search=(
                            SearchVector('name', 'type__name', 'city__name', 'city__region', 'country__name', 'status__name', 'uses__name', 'owner__name', 'former_names', 'description')
                        ),).filter(search=form.cleaned_data['keywords']).distinct('slug')
            if form.cleaned_data['name']:
                qs = qs.annotate(search=(SearchVector('name')),).filter(search=form.cleaned_data['name']).distinct('slug')
            if form.cleaned_data['imo']:
                qs = qs.filter(imo__exact=form.cleaned_data['imo'])
            if form.cleaned_data['type']:
                qs = qs.filter(type__in=form.cleaned_data['type'])
            if form.cleaned_data['year_built_from']:
                qs = qs.filter(year_built__gte=form.cleaned_data['year_built_from'])
            if form.cleaned_data['year_built_to']:
                qs = qs.filter(year_built__lte=form.cleaned_data['year_built_to'])
            if form.cleaned_data['tonnage_from']:
                qs = qs.filter(tonnage__gte=form.cleaned_data['tonnage_from'])
            if form.cleaned_data['tonnage_to']:
                qs = qs.filter(tonnage__lte=form.cleaned_data['tonnage_to'])
            if form.cleaned_data['length_from']:
                qs = qs.filter(length__gte=form.cleaned_data['length_from'])
            if form.cleaned_data['length_to']:
                qs = qs.filter(length__lte=form.cleaned_data['length_to'])
            if form.cleaned_data['beam_from']:
                qs = qs.filter(beam__gte=form.cleaned_data['beam_from'])
            if form.cleaned_data['beam_to']:
                qs = qs.filter(beam__lte=form.cleaned_data['beam_to'])
            if form.cleaned_data['city']:
                qs = qs.annotate(search=(SearchVector('city__name', 'city__region')),).filter(search=form.cleaned_data['city']).distinct('slug')
            if form.cleaned_data['country']:
                qs = qs.filter(country__in=form.cleaned_data['country'])
            if form.cleaned_data['status']:
                qs = qs.filter(status__in=form.cleaned_data['status'])
            if form.cleaned_data['uses']:
                qs = qs.filter(uses__in=form.cleaned_data['uses'])
            if form.cleaned_data['owner']:
                qs = qs.annotate(search=(SearchVector('owner__name')),).filter(search=form.cleaned_data['owner']).distinct('slug')
            if form.cleaned_data['former_names']:
                qs = qs.annotate(search=(SearchVector['former_names']),).filter(search=form.cleaned_data['former_names']).distinct('slug')
            return qs.order_by('slug')

# View all Ships
class AllShipsView(ListView):
    model = Ship

    def get_queryset(self):
        return Ship.objects.all().order_by('slug')

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
