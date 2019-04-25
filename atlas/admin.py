from django.contrib import admin

from atlas.models import Type, City, Country, Status, Use, Owner, Ship

class TypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Type, TypeAdmin)

class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'region')}
admin.site.register(City, CityAdmin)

class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Country, CountryAdmin)

class StatusAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Status, StatusAdmin)

class UseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Use, UseAdmin)

class OwnerAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Owner, OwnerAdmin)

class ShipAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', 'year_built')}
admin.site.register(Ship, ShipAdmin)
