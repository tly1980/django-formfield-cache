

class DummyQueryset:
    """
    Dummy Queryset
    1. Pretend to be a queryset object, but only provide all() method.
    2. Cache the query result at the initial stage
    """

    def __init__(self, queryset):
        self.all_ret = queryset.all()

    def all(self):
        return self.all_ret


def foreignkey_cache(*cache_fields):
    """
    Cache decorators for the Foreignkey.

    Example Usage:

    class EntryAdmin(admin.ModelAdmin):

        @foreignkey_cache('state', 'postcode')
        class AddressAdmin(admin.StackedInline):
            model = Address

        inlines = [AddressAdmin, ]
        list_display = ('first_name', 'last_name', )

    admin.site.register(Entry, EntryAdmin)
    """

    def f(the_admin):
        formfield_for_foreignkey_old = the_admin.formfield_for_foreignkey

        def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
            """
            Get a form Field for a database Field that has declared choices.
            """
            # If the field is named as a radio_field, use a RadioSelect
            if db_field.name in cache_fields and request and request.method == 'GET':
                if '__fkcache' not in request:
                    request.__fkcache = {}

                if db_field.name not in request.__fkcache:
                    request.__fkcache[db_field.name] = DummyQueryset(db_field.formfield(**kwargs).queryset)

                kwargs['queryset'] = request.__fkcache[db_field.name]

            return formfield_for_foreignkey_old(self, db_field, request, **kwargs)

        the_admin.formfield_for_foreignkey = formfield_for_foreignkey

        return the_admin
    return f
