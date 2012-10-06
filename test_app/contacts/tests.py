"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from contacts.models import State, Entry, PostCode
from pyquery import PyQuery as PQ
from django.db import connection
import formfield_cache


class ForeignkeyCacheTest(TestCase):
    def setUp(self):
        u = User.objects.create(username='test', is_active=True, is_superuser=True, is_staff=True)
        u.set_password('1234')
        u.save()
        self.client = Client()
        self.client.login(username='test', password='1234')

    def verify_state(self, resp_content):
        state_supposed_options = [s.state for s in State.objects.all()]
        div_field_states = PQ(resp_content).find('div.field-state')
        e = Entry.objects.get(id=1)
        addresses = e.address_set.all()

        # StackedInline will generate (extra + 1)
        # please view extra: AddressAdmin.extra
        self.assertEqual(len(addresses), len(div_field_states) - 2)

        for div in div_field_states:
            # flatten the html options to a str list
            options_html = [opt_text
                for opt_text in PQ(div).find('option').map(lambda i, e: PQ(e).text())]
            # remove the first option '---------'
            self.assertEqual(options_html[0], '---------')
            options_html.remove('---------')
            self.assertEqual(options_html, state_supposed_options)

    def verify_postcode(self, resp_content):
        postcode_supposed_options = [repr(p) for p in PostCode.objects.all()]
        div_field_postcode = PQ(resp_content).find('div.field-postcode')
        e = Entry.objects.get(id=1)
        addresses = e.address_set.all()
        # StackedInline will generate (extra + 1)
        # please view extra: AddressAdmin.extra
        self.assertEqual(len(addresses), len(div_field_postcode) - 2)

        for div in div_field_postcode:
            # flatten the html options to a str list
            options_html = [opt_text
                for opt_text in PQ(div).find('option').map(lambda i, e: PQ(e).text())]
            # remove the first option '---------'
            self.assertEqual(options_html[0], '---------')
            options_html.remove('---------')
            self.assertEqual(options_html, postcode_supposed_options)

    def test_form_generated_correctly(self):
        """
        Test if the form is being generated correctly
        """
        resp = self.client.get('/admin/contacts/entry/1/')
        self.verify_state(resp.content)
        self.verify_postcode(resp.content)

    def test_cache_being_used(self):
        formfield_cache.decorators.foreignkey_cache_enabled = True
        connection.use_debug_cursor = True
        self.client.get('/admin/contacts/entry/1/')
        queries_changed = [q.get('sql') for q in connection.queries]
        count_postcode_qry = 0
        count_state_qry = 0

        for sql in queries_changed:
            if 'SELECT "contacts_postcode"' in sql:
                count_postcode_qry += 1

            if 'SELECT "contacts_state"' in sql:
                count_state_qry += 1

        self.assertEqual(count_postcode_qry, 1)
        self.assertEqual(count_state_qry, 1)
        connection.use_debug_cursor = False

    def test_cache_not_being_used(self):
        formfield_cache.decorators.foreignkey_cache_enabled = False
        connection.use_debug_cursor = True
        self.client.get('/admin/contacts/entry/1/')
        queries_changed = [q.get('sql') for q in connection.queries]
        count_postcode_qry = 0
        count_state_qry = 0

        # get the count of the queries_changed
        for sql in queries_changed:
            if 'SELECT "contacts_postcode"' in sql:
                count_postcode_qry += 1

            if 'SELECT "contacts_state"' in sql:
                count_state_qry += 1
        connection.use_debug_cursor = False

        e = Entry.objects.get(id=1)
        addresses = e.address_set.all()
        # StackedInline will generate (extra + 1) instances
        # hence the query count is supposed to be: len(addresses) + 2
        self.assertEqual(count_postcode_qry, len(addresses) + 2)
        self.assertEqual(count_state_qry, len(addresses) + 2)

