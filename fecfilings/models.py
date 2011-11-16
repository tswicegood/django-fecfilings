from django.db import models


class Party(models.Model):
    name = models.CharField(max_length=50)


class Candidate(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=200)
    party = models.ForeignKey(Party)

    # TODO: can this be made a foreign key?
    incumbent = models.CharField(max_length=20)

    # Precalculated totals from the FEC
    total_receipts = models.IntegerField()
    total_individual = models.IntegerField()
    total_pac = models.IntegerField()
    total_party = models.IntegerField()
    total_candidate = models.IntegerField()

    disbursements = models.IntegerField()
    cash_on_hand = models.IntegerField()
    debt = models.IntegerField()

    date_through = models.DateField()

    committee_calendar_year = models.IntegerField()
    transfers = models.IntegerField()


class Contributor(models.Model):
    name = models.CharField(max_length=250)
    employer = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    date = models.DateField()
    amount = models.IntegerField()

    # Fields that don't appear to have anything in them
    memo_code = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
