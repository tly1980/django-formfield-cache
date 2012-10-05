from django.db import models


class State(models.Model):
    state = models.CharField(max_length=128)


class PostCode(models.Model):
    code = models.CharField(max_length=128)


# Create your models here.
class Address(models.Model):
    state = models.ForeignKey(State)
    postcode = models.ForeignKey(PostCode)


class Person(models.Model):
    address = models.ForeignKey(Address)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    mobile = models.CharField(max_length=128)
