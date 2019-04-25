from django.urls import path
from atlas import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ship/<slug:slug>/', views.ShipDetailView.as_view(), name='ship_detail'),
    path('ships/', views.ShipListView.as_view(), name='ships'),
    path('type/<slug:slug>/', views.TypeDetailView.as_view(), name='type_detail'),
    path('city/<slug:slug>/', views.CityDetailView.as_view(), name='city_detail'),
    path('country/<slug:slug>/', views.CountryDetailView.as_view(), name='country_detail'),
    path('status/<slug:slug>/', views.StatusDetailView.as_view(), name='status_detail'),
    path('use/<slug:slug>/', views.UseDetailView.as_view(), name='use_detail'),
    path('owner/<slug:slug>/', views.OwnerDetailView.as_view(), name='owner_detail'),
]
