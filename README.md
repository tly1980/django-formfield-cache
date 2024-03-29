---
Author: Tom Tang
---

django-formfield-cache
============================

Prevent unnecessary DB hit of the foreign key field of InlineAdmin subclass (StackedAdmin/TabularAdmin).
Each foreign key field of the EVERY instance of InlineAdmin subclass (StackedAdmin/TabularAdmin), will cause one database hit.

django-formfield-cache provide a **simple** and **non-intrusive** way (using decorators) to cache the queries from foreign key fields of any inlineAdmin subclasses.


Example: 
--------

```python
# state, postcode is a foreignkey field of Address model.
# without @foreignkey_cache, unnessary DB query will be generated 
# against EVERY foreignkey filed of EVERY instance of inlineadmin
@foreignkey_cache('state', 'postcode') 
class AddressAdmin(admin.StackedInline):
    model = Address
    ...
    ...
```

***

Before and after applying the cache
================================

Entry Admin has a AddressAdmin (extended from StackedInlineAdmin).
In this particular instance of entry, it has 6 instances of AddressAdmin

***Before, it cost 18 queries.***

A few duplicated query of state and postcode. Every instance of StackedInline will trigger the query.

![Query Count](https://raw.github.com/tly1980/django-formfield-cache/release/0.3/screenshots/qry_count.png)

![Query Generated](https://raw.github.com/tly1980/django-formfield-cache/release/0.3/screenshots/qry_actual.png)


***After, it cost only 6 queries.***

The unnessary queries has been removed, and StackedInline is hitting the cache.

![Query Count](https://raw.github.com/tly1980/django-formfield-cache/release/0.3/screenshots/qry_count_after.png)

![Query Generated](https://raw.github.com/tly1980/django-formfield-cache/release/0.3/screenshots/qry_actual_after.png)

***

Full Example Code 
=================

The complete source code can be found in test_app


models.py
---------
```python
class State(models.Model):
    state = models.CharField(max_length=128)

    def __repr__(self):
        return self.state

    def __str__(self):
        return repr(self)


class PostCode(models.Model):
    code = models.CharField(max_length=128)
    town = models.CharField(max_length=128)

    def __repr__(self):
        return "%s (%s)" % (self.code, self.town)

    def __str__(self):
        return repr(self)


class Entry(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=128)


class Address(models.Model):
    state = models.ForeignKey(State)
    postcode = models.ForeignKey(PostCode)
    street = models.CharField(max_length=128)
    entry = models.ForeignKey(Entry)
```

admin.py
--------

```python
class EntryAdmin(admin.ModelAdmin):

    @foreignkey_cache('state', 'postcode')
    class AddressAdmin(admin.StackedInline):
        model = Address

    inlines = [AddressAdmin, ]
    list_display = ('first_name', 'last_name', )

admin.site.register(Entry, EntryAdmin)
```    
