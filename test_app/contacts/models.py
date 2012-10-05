from django.db import models


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

