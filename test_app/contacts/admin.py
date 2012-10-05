from django.contrib import admin
from models import Entry, State, PostCode, Address
from decorators import fkcache


class PostCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'town', )
    pass


class StateAdmin(admin.ModelAdmin):
    list_display = ('state', )


@fkcache('state', 'postcode')
class AddressAdmin(admin.StackedInline):
    model = Address


class EntryAdmin(admin.ModelAdmin):
    inlines = [AddressAdmin, ]
    list_display = ('first_name', 'last_name', )


admin.site.register(PostCode, PostCodeAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Entry, EntryAdmin)
