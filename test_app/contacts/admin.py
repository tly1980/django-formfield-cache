from django.contrib import admin
from models import Entry, State, PostCode, Address
from formfield_cache import foreignkey_cache


class PostCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'town', )
    pass


class StateAdmin(admin.ModelAdmin):
    list_display = ('state', )


class EntryAdmin(admin.ModelAdmin):

    @foreignkey_cache('state', 'postcode')
    class AddressAdmin(admin.StackedInline):
        extra = 1
        model = Address

    inlines = [AddressAdmin, ]
    list_display = ('first_name', 'last_name', )


admin.site.register(PostCode, PostCodeAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Entry, EntryAdmin)
